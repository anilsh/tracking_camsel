
# Intelligent Camera Selection Decisions for Target Tracking in a Camera Network
** PyTorch implementation of our paper titled _Intelligent Camera Selection Decisions for Target Tracking in a Camera Network_, WACV 2022 

_Anil Sharma, Saket Anand, Sanjit K. Kaul_

[[Paper](https://www.computer.org/csdl/proceedings-article/bigmm/2020/09232593/1o56ALOzkeA)] [[BibTeX](https://www.computer.org/csdl/api/v1/citation/bibtex/proceedings/1o56xuliEpi/09232593)]

---
Camera selections were shown to be highly crucial for target tracking in a camera network but learning a camera selection policy is highly challenging for larger camera networks. In this work, we show the efficacy of representation learning to reduce training time and to improve camera selection performance.

---

## Code

The code is organized as follows:
1. ```main_q_dbx_icaps.m``` is the main file to call training and testing function for a sub-dataset x. Please note that sub-dataset-1 and 2 share same network topology and hence only one model is trained for both. 
2. All folder names are self-explanatory and you don't need to edit any of the file inside any folder to reproduce the results.

## Downloading the data

### NLPR MCT benchmark dataset

Download the dataset from the [[official website](http://mct.idealtest.org/Datasets.html)] . This dataset contains four sub-datasets and we have used all four in our method.

---

## Running the tracker

Edit the variable ```task``` in the main file of a particular sub-dataset (```task=2``` is for testing with ground truth re-id). To simulate errors in re-identification, change ```task``` and edit ```opts.fpath``` in the main file to point the location of the ground-truth file.


### Dependencies

The code should run with basic matlab functions and doesn't require any sophisticated installation. 

### Pre-trained model

The pre-trained model and results for each specific case of the simulation are provide in 'model' and 'results_icaps' directories respectively. 

### Tables and Figures
In folder 'metric', you will find various scripts to reproduce all tables and figures reported in the paper. Use [MCT evaluation kit](http://mct.idealtest.org/Datasets.html) to generate MCTA values from the results file. Result files are kept in ```results_icaps``` folder for every case. 


### Training

To train a model from scratch, set ```task=0``` in the main file. Edit epochs, the provided model was trained for 50K epochs. Since it is a table based method and it is not possible to include all possible cases so we have set maximum value of the ```telapse``` to be 200 and the policy behaves randomly after reaching this value.

### Visualization

To reproduce figure 4 of the paper. Edit the scripts in the train folder and uncomment following lines. Set first argument of subplot accordingly. 
```
    subplot(length(pALL(2:2:end)),1,rs_cnt);
    a= [(repmat(gt_cam_allt',100,1)); zeros(5,length(gt_cam_allt)); (repmat(pr_cam_allt',100,1))];
    colormap('hot');
    imagesc(a);
    set(gca,'ytick',50:100:200)
    set(gca,'yticklabel',{'GT','Sel'})

```


## Remarks

The related method are multi-camera multi-target and our method is multi-camera single target tracking. For fair comparison, we have run multiple parallel iterations of our method one for each target of the test set to make it multi-camera multi-target approach.


## Extension and improvement in results

We have extended the proposed approach by including random jumps in the exploration of the target's trajectory during training. This has provided significant improvement in accuracy, precision and recall. The code is available on request. 

We have also used a re-identification implementation  of [[this paper](https://github.com/layumi/Person_reID_baseline_matconvnet)] to replace ```isTargetPresent()``` function used in training and testing functions. We are not providing the code but you are encouraged to use the linked implementation. 


If this code helps your research, please cite the following work which made it possible.

```
@inproceedings{sharmaScheduleCameras,
  title =        {Reinforcement Learning based Querying in Camera Networks for Efficient Target Tracking},
  author =       {Sharma, Anil and Anand, Saket and Kaul, Sanjit},
  booktitle =    {ICAPS},
  year =         {2019}
}

@INPROCEEDINGS {9232593,
author = {A. Sharma and M. K. Pal and S. Anand and S. K. Kaul},
booktitle = {2020 IEEE Sixth International Conference on Multimedia Big Data (BigMM)},
title = {Stratified Sampling Based Experience Replay for Efficient Camera Selection Decisions},
year = {2020},
pages = {144-151},
doi = {10.1109/BigMM50055.2020.00029},
url = {https://doi.ieeecomputersociety.org/10.1109/BigMM50055.2020.00029},
publisher = {IEEE Computer Society}
}



```

## License

This code is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Some external dependencies have their own license.

