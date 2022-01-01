import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class AuxiliaryFunction:

    def __init__(self, num_camera=5, d=10, te_len=10, h_len=10):
        self.img_size = (320,240)
        self.num_camera = num_camera
        self.d = d
        self.te_len = te_len
        self.h_len = h_len
        
    def make_one_hot_camera(self, val):
        enc = np.zeros((self.num_camera))
        enc[val] = 1
        
        return enc
        
    def find_curr_rt(self, bbox):
        #print (bbox)
        d = self.d
        [r1,rx1,ry1] = self.get_region_num(bbox[0],bbox[1])
        [r2,rx2,ry2] = self.get_region_num(bbox[0]+bbox[2],bbox[1]+bbox[3])

        #print (rx1,ry1,rx2,ry2)
        rt = np.zeros((d,d))
        rt[rx1:rx2+1,ry1:ry2+1] = 1

        return rt

    def get_region_num(self, x,y):
        d = self.d
        cell_size = np.array(self.img_size)/d

        # find regions for x and y direction
        rx = np.floor( x / cell_size[0] )
        ry = np.floor( y / cell_size[1] )
        #if (rx <=0 or ry <= 0):
        #    print (rx,ry,x,y,cell_size)
        #    print ('Error in get_region_num')
        #    return

        r = d*(rx-1) + ry
        return r,np.int(rx),np.int(ry)

    def find_target_camera(self, ped,frameNum):
        myc = -1
        for c in range(self.num_camera):
            cidx = ped[np.logical_and(ped[:,0]==c, ped[:,1] == frameNum), :]
            #print ('cidx: ',cidx)
            if cidx.shape[0]>0:
                myc = c
                break

        if myc == -1:
            myc = self.num_camera-1
        return myc

    ''' Function to find the initial state given initial location'''
    def initial_state(self,pos,rt_req=np.array([-1,1])):
        # find current camera (one-hot encoding)
        d = self.d
        ct = np.zeros((self.num_camera,1))
        ct[pos[0]] = 1
        # find region 
        rt = self.find_curr_rt(pos[2:]) if rt_req.shape[0]<d else rt_req
        # time-elapse 
        te = np.zeros((self.te_len,1))
        te[0] = 1

        #print (ct,rt,te)
        # combine all elements
        state = np.concatenate((ct, rt.reshape(d*d,1)))
        state = np.concatenate((state, te))

        #print (state)
        #print (state.astype(np.float).ravel())

        return state #state.astype(np.float).ravel()

    ''' updates history by appending previous state'''
    def update_history(self,history, prev_state):
        ''' append previous_state to the history '''
        num_camera = self.num_camera
        d = self.d
        history['c'][1:,] = history['c'][0:-1,]
        history['c'][0,] = prev_state[0:num_camera].ravel()

        history['r'][1:,] = history['r'][0:-1,]
        history['r'][0,] = prev_state[num_camera: num_camera+d*d].ravel()

        history['te'][1:,] = history['te'][0:-1,]
        history['te'][0,] = prev_state[num_camera+d*d:].ravel()

        return history

    ''' updates state and history based on the camera selected '''
    def update_state_and_history(self, history, te,curr_c,prev_c, curr_state,rt, ispresent,dte):
        d = self.d
        te_len = self.te_len
        num_camera = self.num_camera
        te_val = np.int(np.ceil(te/dte ))
        #print ('telapse: ',te, 'te_val: ',te_val)
        if ispresent:
            # update state [update history if telaspe > te_len]
            if te_val < te_len and prev_c==curr_c:
                # update only state and rt_history
                next_state = curr_state
                nte = np.zeros((te_len,1))
                nte[te_val] = 1
                next_state[num_camera+d*d:] = nte

                # change rt in history
                history['r'][1:,] = history['r'][0:-1,]
                history['r'][0,] = next_state[num_camera:num_camera+d*d].ravel()
                # add new rt to state
                next_state[num_camera:num_camera+d*d] = rt.reshape(d*d,1)
            elif prev_c == curr_c:
                # add to history and then update state
                history = self.update_history(history, curr_state)
                pinfo = [curr_c,0]
                next_state = self.initial_state(pinfo,rt)
            elif np.argmax(curr_state[0:num_camera]) == curr_c:
                # [re-appeared] do not clear rt_history (rest all same as prev_c != curr_c)
                history = self.update_history(history, curr_state)
                pinfo = [curr_c,0]
                next_state = self.initial_state(pinfo,rt)
                
            else:
                history = self.update_history(history, curr_state)
                pinfo = [curr_c,0]
                next_state = self.initial_state(pinfo,rt)
                # initialize all rt_history to zero
                history['r'] = np.zeros((self.h_len,d*d))
        else: # target not present in selected camera
            # update only history with new selection
            if np.argmax(history['c'][0,]) == curr_c and (history['c'][0,0] != 1 and curr_c == 0):
                #print ('1st')
                tmp_state = self.initial_state([curr_c,0],np.zeros((d,d)))
                history = self.update_history(history, tmp_state)
                next_state = curr_state

            elif np.argmax(history['c'][0,]) == curr_c and te_val < te_len:
                #print ('2nd')
                nte = np.zeros((te_len,1))
                nte[te_val] = 1
                history['te'][0,] = nte.ravel()
                next_state = curr_state
            else:
                #print ('3rd')
                tmp_state = self.initial_state([curr_c,0],np.zeros((d,d)))
                history = self.update_history(history, tmp_state)
                next_state = curr_state

        return history, next_state

    #def take_action(curr_state, action,history):

    ''' discounts reward'''
    def discount_rewards(self,r):
        """ take 1D float array of rewards and compute discounted reward """
        gamma = 0.90 # discount factor for reward
        
        r = r.astype(np.float).ravel()
        discounted_r = np.zeros_like(r)
        running_add = 0
        for t in reversed(xrange(0, r.size)):
            if r[t] == 1: running_add = 0 # reset the sum, since here target reached correct camera
            running_add = running_add * gamma + r[t]
            discounted_r[t] = running_add
        return discounted_r

    def load_image(self, ped,c,fno,db_no):
        # find bounding box
        bbox = ped[ np.logical_and(ped[:,0]==c,ped[:,1]==fno),2:]
        #print (bbox)
        if bbox.shape[0] == 0:
            bbox = []
            ispresent = 0
        else:
            if bbox.shape[0] > 1:
                print (bbox)
                print (bbox.shape)
            bbox = bbox[0]
            ispresent = 1
            
        # read image
        if c != self.num_camera-1:
            dbPath = '/media/win/data/MCT dataset/dataset'+str(db_no)
            if db_no == 3:
                imgName = dbPath+'/cam'+str(c+1)+'/'+format(fno+1,'04d')+'.png'
            elif db_no == 4:
                imgName = dbPath+'/cam'+str(c+1)+'/'+format(fno+1,'05d')+'.png'
            img = [] #Image.open(imgName)
        else:
            img = []
        #print (bbox, img.size)
        
        return img,bbox,ispresent
    
    def compute_num_frames(self, p,g):
        total_fr = np.sum(p != self.num_camera-1)
        ict_fr = np.sum( p[g == self.num_camera-1] != self.num_camera-1)

        return total_fr, ict_fr

    def compute_MCTA(self, p,g):
        # compute handovers in SCT
        tot = 0
        handover = 0
        for i in range(len(g)-1):
            if g[i+1] == g[i] and g[i] != (self.num_camera-1):
                handover += np.sum(p[i+1] != p[i])
                tot += 1
        if tot == 0:
            h_sct = 1
        else:
            h_sct = 1 - np.float(handover)/tot

        # compute handovers in ICT
        tot = 0
        handover = 0
        for i in range(len(g)-1):
            if g[i+1] != g[i] or g[i] == (self.num_camera-1):
                handover += np.sum(p[i+1] != p[i])
                #print (handover)
                tot += 1
        if tot == 0:
            h_ict = 1
        else:
            h_ict = 1 - np.float(handover)/tot

        # compute confusion matrix
        M = np.zeros((self.num_camera,self.num_camera), dtype=float)
        for i in range(self.num_camera):
            for j in range(self.num_camera):
                M[i,j] = np.sum( np.logical_and(g == i, p == j) )
        # compute precision, recall
        P,R = [],[]
        for i in range(self.num_camera):
            if np.sum( M[:,i] ) != 0:
                P.append( M[i,i]/ np.sum( M[:,i] ))
            if np.sum( M[i,:] ) != 0:
                R.append(M[i,i]/ np.sum( M[i,:] ))
        P = np.mean(P)        
        R = np.mean(R)
        # compute f1-score
        f1 = 2*P*R/(P+R)
        # compute MCTA
        mcta = f1 * h_sct * h_ict

        return mcta,f1,P,R,h_sct,h_ict
    
    def plot_color_transitions(self, p,g):
        rep_len = 50
        # replicate array
        adata = np.vstack((np.array(list(p)*rep_len).reshape(rep_len,-1),\
                        np.array(list(g)*rep_len).reshape(rep_len,-1)))
        # plot figure
        fig = plt.figure(figsize=(40,2))
        ax = plt.axes()
        c = ax.pcolor(adata)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(20) 
        plt.show()

    def compute_num_frames_pi(self, p,g):
        Cx = self.num_camera-1
        count_ict = 0
        val = np.zeros((3))
        n = 0
        t = 0
        inc = 1
        #y = p[g != num_camera-1]
        y = np.nonzero(g != Cx)[0]
        #print (val)
        #return y
        for i in range(y[-1]):
            if inc==1 and g[i] != Cx:
                # do nothing, inside a camera FOV
                aa = 1  # dummy variable
            elif inc==0 and g[i]==p[i] and g[i]!=Cx:
                # entering in a camera FOV
                count_ict += 1
                inc = 1
            elif inc == 1 and g[i] == Cx:
                # moving out of a camera FOV
                inc = 0
                t += 1
                n += p[i] != Cx
            else:
                t += 1
                n += p[i] != Cx
        val[0] = t
        val[1] = n
        val[2] = count_ict

        return val

    def compute_APRF_one_person_ict(self, p,g):
        nfPi = self.compute_num_frames_pi(p,g) # stores total_frames, #frames processed, total transitions found
        #return nfPi
        g_nc = g[1:] - g[0:-1]
        total_tr = np.sum( g_nc != 0)
        Cx = self.num_camera-1
        # compute accuracy
        A = np.mean( (nfPi[0]-nfPi[1])/nfPi[0] )
        # compute precision
        P = np.mean( (nfPi[2])/nfPi[1] )
        # compute recall
        R = np.mean( (nfPi[2])/total_tr )
        # compute F
        F = np.sum([g[i]==Cx and p[i]!=Cx for i in range(len(p))])

        return A,P,R,F, total_tr

    def compute_APRF_one_person_sct_ict(self, p,g):
        Cx = self.num_camera-1
        #return nfPi
        g_nc = g[1:] - g[0:-1]
        total_tr = np.sum( g_nc != 0)
        # compute accuracy
        A = np.sum([p[i]==g[i] for i in range(len(p))])/len(g)
        # compute precision
        P = np.sum([p[i]==g[i] and p[i]!=Cx for i in range(len(p))])/np.sum([x!=Cx for x in p])
        # compute recall
        R = np.sum([p[i]==g[i] and g[i]!=Cx for i in range(len(p))])/np.sum([x!=Cx for x in g])
        # Compute F
        F = np.sum([g[i]==Cx and p[i]!=Cx for i in range(len(p))]) + np.sum([p[i]!=g[i] and p[i]!=Cx and g[i]!=Cx for i in range(len(p))])

        return A,P,R,F, total_tr
        