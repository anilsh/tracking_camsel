import scipy.io as spio
import numpy as np

def get_pid(set_no=3, train_flag='train'):
    if set_no == 1:
        [foldr, pid] = get_set1(train_flag)
        num_camera = 3
        alltime = 24000
        fps = 20
    elif set_no == 2:
        [foldr, pid] = get_set2(train_flag)
        num_camera = 3
        alltime = 24000
        fps = 20
    elif set_no == 3:
        [foldr, pid] = get_set3(train_flag)
        num_camera = 4
        alltime = 5251
        fps = 25
    elif set_no == 4:
        [foldr, pid] = get_set4(train_flag)
        num_camera = 5
        alltime = 36000
        fps = 25
    elif set_no == 5: # dukeMTMC dataset
        [foldr, pid] = get_setDuke(train_flag)
        num_camera = 8
        alltime = 356648
        fps = 60
    elif set_no == 6: # whole AICity dataset
        [foldr, pid] = get_AICity(train_flag)
        num_camera = 40
        alltime = 356648
        fps = 10
    elif set_no == 7: # only scenario-4 of AICity dataset
        [foldr, pid] = get_AICity_S04(train_flag)
        num_camera = 25
        alltime = 356648
        fps = 10
    elif set_no == 8: # WNMF dataset
        [foldr, pid] = get_WNMF_train_test(train_flag)
        num_camera = 15
        alltime = -1
        fps = 5
        
    # load dataset
    if set_no == 5:
        X = spio.loadmat(foldr)
        print ('Total number of person in data set: ', X['PID_copy'].shape)
        pALL = X['PID_copy'][0,pid]
    elif set_no == 6:
        X = spio.loadmat(foldr)
        print ('Total number of person in data set: ', X['PID'].shape)
        pALL = X['PID'][0,:]   # all PIDs are used for training/testing [one scenario is train, other is test]
    elif set_no != 7 and set_no != 8:
        X = spio.loadmat(foldr)
        print ('Total number of person in data set: ', X['PID'].shape)
        pALL = X['PID'][0,pid]
    else:
        print ('Total number of person in data set: ', pid.shape)
        pALL = pid
    
    return pALL,num_camera,alltime,fps

def get_set1(flag):
    foldr = '../data/ann_MCT_dataset1_pidWise.mat'
    pALL=np.array([88,137,182,223,174,71,200,58,1,185,74,168,235,46,17,67,162,100, \
        192,113,140,6,94,81,11,181,159,78,147,22,127,115,68,143,59,212,217,161, \
        92,164,227,206,73,123,125,126,230,233,83,197,231,34,145,26,114,27,138,7,\
        151,8,48,120,166,215,35,85,64,111,156,225,65,171,153,25,45,207,219,178,\
        23,165,50,199,110,203,211,47,152,30,132,102,205,96,89,129,52,107,60,36,\
        216,167,87,149,208,116,213,57,41,214,12,175,163,15,173,144,134,86,194,82,\
        128,186,63,105,122,69,21,183,169,187,222,19,232,108,198,79,141,91,51,150,\
        53,77,5,119,39,33,170,84,229,180,133,40,188,139,54,121,158,55,42,10,9,124,\
        142,90,136,189,226,131,135,13,95,24,209,191,44,29,16,218,20,93,184,130,117,\
        49,204,3,112,146,195,109,62,37,98,154,72,99,157,234,103,56,106,31,66,172,202,\
        38,43,28,101,221,193,177,2,4,160,155,14,210,196,176,97,70,201,228,75,18,104,\
        179,118,148,190,224,220,32,61,80,76])-1

    if flag == 'test':
        pid = pALL[1::2] 
    elif flag == 'train':
        pid = pALL[0::2]
    else:
        pid = pALL
        
    return foldr,pid

def get_set2(flag):
    foldr = '../data/ann_MCT_dataset2_pidWise.mat'
    pALL = range(255) #np.random.permutation(255)
    if flag == 'test':
        pid = pALL[0:] 
    elif flag == 'train':
        pid = pALL[0::2] 
    else:
        pid = pALL
        
    return foldr,pid

def get_set3(flag):
    foldr = '../data/ann_MCT_dataset3_pidWise.mat'
    pALL = np.array([9,1,5,2,8,7,6,12,13,11,4,14,10,3])
    pALL = pALL - 1
    if flag == 'test':
        pid = pALL[1::2] 
    elif flag == 'train':
        pid = pALL[0::2] 
    else:
        pid = pALL
        
    return foldr,pid

def get_set4(flag):
    foldr = '../data/ann_MCT_dataset4_pidWise.mat'
    pALL = np.array([1,46,17,6,11,22,34,26,27,7,8,48,35,25,45,23,47,30,36,41,12,15,21,19,5,39,\
            33,40,42,10,9,13,24,44,29,16,20,49,3,37,31,38,43,28,2,4,14,18,32])-1
    if flag == 'test':
        pid = pALL[1::2] 
    elif flag == 'train':
        pid = pALL[0::2] 
    else:
        pid = pALL
       
    return foldr,pid
        
def get_setDuke(flag):
    #foldr = '../data/ann_DukeDataset_pidWise.mat'
    foldr = '../data/ann_duke_sync_seq.mat'
    pALL = spio.loadmat('../data/pALL_DukeDataset_rand.mat')  # load the random PIDs
    pALL = pALL['pALL']-1
    if flag == 'test':
        pid = pALL[0,1::2] 
    elif flag == 'train':
        pid = pALL[0,0::2] 
    else:
        pid = pALL
        
    return foldr,pid

def get_AICity_S04(flag):
    foldr = '../data/ann_AICity2019_train_pidWise_S04.mat'
    pALL = spio.loadmat('../data/ann_AICity2019_train_pidWise_S04.mat')
    pALL = pALL['PID']
    if flag == 'test':
        pid = pALL[0,1::2] 
    elif flag == 'train':
        pid = pALL[0,0::2] 
    else:
        pid = pALL

    return foldr,pid
    
def get_AICity(flag):
    
    if flag == 'test':
        #foldr = '../data/ann_AICity2019_test_pidWise_mm.mat'
        foldr = '../data/ann_AICity2019_test_pidWise_mm_s05.mat'
    elif flag == 'train':
        #foldr = '../data/ann_AICity2019_train_pidWise_ALL.mat'
        foldr = '../data/ann_AICity2019_train_pidWise_mm_s04.mat'
    pid = -1
    
    return foldr,pid
    
def get_WNMF_train_test(flag):
    #file_train = '/media/8tb/abstraction/wnmf/data/PED_wnmf_cross_match_train.mat'
    #file_test = '/media/8tb/abstraction/wnmf/data/PED_wnmf_cross_match_test.mat'
    file_train = '../data/PED_wnmf_cross_match_train.mat'
    file_test = '../data/PED_wnmf_cross_match_test.mat'
    pALL_train = spio.loadmat(file_train)
    pALL_test = spio.loadmat(file_test)
    pALL_train = pALL_train['PED']
    pALL_test = pALL_test['PED']
    if flag == 'test':
        pid = pALL_test[0,:]
    elif flag == 'train':
        pid = pALL_train[0,:]
    else:
        pid = pALL_train[0,:]

    return file_train,pid
    