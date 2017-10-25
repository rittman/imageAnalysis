library(brainwaver)

doWave <- function(p){
 ts <- read.table(paste("FUNCTIONAL_ppm_std_2mm",p,"ts.txt",sep="_")) # import timeseries
 ts.mat <- as.matrix(ts) # convert dataframe to matrix
 ts.mat.t <- t(ts) # rotate matrix

 parcelDir = paste("adjMat", p, sep="")
 dir.create(parcelDir, showWarnings=FALSE)
 setwd(parcelDir)
 adjMat <- const.cor.list(ts.mat.t, export.data=TRUE) 
 setwd("../")
 return(p)
}

lapply(seq(100,500,by=100),doWave)
