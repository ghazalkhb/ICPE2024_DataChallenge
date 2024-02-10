# 2024 ICPE Data Track Project
<h3>Description</h3>
<div>This repository is the implementation of the "" paper. You can download an run each file of codes and see the result. The data set used in this project can be found at this link: 

    
<h3>How to run this project?</h3>
To facilitate the process, you should follow these steps:
<br></ber>(https://github.com/alibaba/clusterdata/tree/master/cluster-trace-microservices-v2022)

<br><b>Step 1:</b> Run the "PreProcessing.py" file. Make sure that changes some part of the code that is necessary (For example file paths). This code will edit the row data and extract the data we need to use for this project. Some columns emitted in this code and we skipped some noises (as bad lines).


<b>Step 2:</b> Now you should run the "Services.py" code. In this program, we filtered our data based on the services and then randomly chose 100 of them and saved them in a new file.

<b>Step 3:</b> Then you should run the "Louvain.py" code for the community detection part. This code will open the files we made in the previous step and make graphs from them. Next, it would run the Louvain method (which is a community detection method) on every graph. At the final stage, it would save the result as a CSV file and also save the graphs with their community classes as an image.

<b>Step 4:</b> For finding similarity between graphs you should run the "Similarity.py" code. In this code, we will apply the K-means method to all the graphs we made in the second step. Then we calculate the similarity between every pair and print them. For finding the optimal K for the K-mean algorithm we used the "Elbow.py" file. Also, we evaluate the K-mean algorithm on this dataset by Silhouette score.
