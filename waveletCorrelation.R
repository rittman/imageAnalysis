library(brainwaver)

# function to perform Fisher R to Z transform
doFtoZ <- function(x,adjMat){
 rho = adjMat[[x]]
 # set diagonal to NA
 for(x in seq(length(rho[1,]))){
  for(y in seq(length(rho[,1]))){
   if(x == y){
    rho[x,y] = NA
   }
  }
 }
 adjMat <- fisherz(rho)
 adjMat[[x]] <- 0.5*log((1+rho)/(1-rho))
 outFile = past(paste("adjMat", x, sep="_"),".txt", sep="")
 write.table(adjMat, outFile, col.names=FALSE, row.names=FALSE)
 return(rho)
}

doWave <- function(p){
 ts <- read.table(paste("FUNCTIONAL_ppm_std_2mm",p,"ts.txt",sep="_")) # import timeseries
 ts.mat <- as.matrix(ts) # convert dataframe to matrix
 ts.mat.t <- t(ts) # rotate matrix

 # define output directory
 parcelDir = paste("adjMat", p, sep="")

 # create the outputdirectory
 dir.create(parcelDir, showWarnings=FALSE)

 # go to subject's directory
 setwd(parcelDir)

 # obtain wavelet cross correlations
 adjMat <- const.cor.list(ts.mat.t, export.data=FALSE) 

 # define list of wavelet scales
 dList=list("d1","d2","d3","d4")
 
 # do Fisher transform and write to a file
 sapply(dList,doFtoZ,adjMat=adjMat)

 # return to the working directory
 setwd("../")
 return(p)
}

lapply(seq(100,500,by=100),doWave)
