
# Intelligent Camera Selection Decisions for Target Tracking in a Camera Network
** PyTorch implementation of our paper titled _Intelligent Camera Selection Decisions for Target Tracking in a Camera Network_, WACV 2022 

_Anil Sharma, Saket Anand, Sanjit K. Kaul_

[[Paper](https://openaccess.thecvf.com/content/WACV2022/papers/Sharma_Intelligent_Camera_Selection_Decisions_for_Target_Tracking_in_a_Camera_WACV_2022_paper.pdf)] [[BibTeX](https://openaccess.thecvf.com/content/WACV2022/html/Sharma_Intelligent_Camera_Selection_Decisions_for_Target_Tracking_in_a_Camera_WACV_2022_paper.html)]

---
Camera selections were shown to be highly crucial for target tracking in a camera network but learning a camera selection policy is highly challenging for larger camera networks. In this work, we show the efficacy of representation learning to reduce training time and also to improve camera selection performance. We also train the RL policy in a semi-supervised way.

---

## Code

The code is organized as follows:
1. ```scripts``` is the main folder from where training and testing scripts can be found. All codes are in jupyter notebook. It also contains notebook to reproduce the plots from the paper. It has four subfolders, supervised: for training/testing a policy with supervised training, semisup: for training in a semi-supervised manner, unsupervised: for training in an unsupervised way using a re-id based method, and representation: includes models trained for auto-encoder.
2. ```data``` It contains data files for all datasets (all 4 sets of NLPR MCT, Duke). It also contains scripts to read these data files and also the training testing split as used in our ICAPS [paper](https://github.com/anilsh/scheduleQueries). Original images of the dataset can be downloaded from the dataset website. 
3. ```results``` It contains all results of our paper that can be used to generate the tables and figures of the paper

## Downloading the data

### NLPR MCT benchmark dataset

Download the dataset from the [[official website](http://mct.idealtest.org/Datasets.html)] . This dataset contains four sub-datasets and we have used all four in our method.
We have converted all datasets into trajectory files and only these are used by our method. These are placed in ```data``` folder and necessary scripts are provided to read the files and training/testing split.

---

## Running the tracker

In scripts folder, run ```TEST_{script_name}.ipynb```  to run with the pretrained models, the script runs for NLPR set-4. To change the dataset, change the variable ```db_no```. The details of the dataset can be checked from ```get_pid_test_train.py``` in data folder.  


### Dependencies

The code requires pytorch 1.1.0 and jupyter notebook (should work well with Python 3.5). Apart from it, you need to install scipy, matplotlib, numpy and hickle for loading and plotting purposes. 

### Pre-trained model

The pre-trained model and results for each specific case of the simulation are provide in 'models' . 

### Tables and Figures
In folder 'plots', you will find various scripts to reproduce all tables and figures reported in the paper. Use [MCT evaluation kit](http://mct.idealtest.org/Datasets.html) to generate MCTA values from the results file. Result files are kept in ```results_icaps``` folder for every case. 


### Training

To train a model from scratch, use notebooks in any of the folder (supervised/semisup/unsupervised)  to train SER based policy for NLPR set-4. To train for a different dataset, change ```db_no``` in the notebook accordingly. 

The folder representation contains pre-trained AE models which needs to be used with every type of training to include latent representation of the history vector.

---

If this code helps your research, please cite the following work which made it possible.

```
@InProceedings{Sharma_2022_WACV,
    author    = {Sharma, Anil and Anand, Saket and Kaul, Sanjit K},
    title     = {Intelligent Camera Selection Decisions for Target Tracking in a Camera Network},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
    month     = {January},
    year      = {2022},
    pages     = {3388-3397}
}

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

