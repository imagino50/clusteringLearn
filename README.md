# Data stream 'Density-based Clustering' in real time   

## Project purpose  
Detect 'density-based clustering' of a continuous (infinite) stream of 'Events'.  
'Event' attributes : posX, posY, intensity, radius, clusterId, clustererProbability, clusterExemplar

The classification of these 'events' is done accordingly to these 3 conditions :
- Events are sent one by one to the stream input
- Each event intensity decreases while its radius increases over time.  
- Events with weak intensity are filtered

## Steps Process  
1. Generates continously 'events' as 2D input : Randomly or from a standard deviation around a moving center. 
2. Draws and update 'events' according to the density-based clustering 

## How to run  

```
git clone https://github.com/imagino50/clusteringLearn.git
```
```
npm install
```
```
python main.py
```

## Dependency
- numpy 
- pandas
- collections
- seaborn
- matplotlib


