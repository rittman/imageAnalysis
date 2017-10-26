# Script to apply the Fisher r to z transform. Instructions here:
# 1. make sure you have the psych package installed using: install.packages("psych")
# 2. ensure you've run R or set the working directory as your root directory for the project
# 3. open R
# 4. type: source("doFtoZ.R")
# 5. err, that's it...
# 6. contact me when it doesn't work.


library(psych)

rtoz <- function(dName, wf="wave_cor_mat_level_2d_500.txt"){
  # get filename
  fname = paste(dName,wf,sep="/")
  
  if(file.exists(fname)){
    print(fname)
    
    # import file
    aa = read.table(fname, na.strings = c("NaN", "NA", "nan"))
    
    # set output name
    out = paste(".",strsplit(fname,"\\.")[[1]][2],
                "_z", ".txt", sep="")
    print(out)
    
    # set diagonal to NA
    for(x in seq(length(aa[1,]))){
     for(y in seq(length(aa[,1]))){
      if(x == y){
       aa[x,y] = NA
      }
     }
    }
 
    # do Fisher's r to z transform
    bb = fisherz(aa)
    
    # write out, trasnsposing matrix to retain columns and rows
    write(t(bb), file=out, ncolumns = length(bb[,1]), sep=" ")
  } else {
    return(paste(fname, "doesn't exist"))
  }

}

# set the list of diagnoses, the script below searches recursively for directories within each diagnosis directory
#print(list.dirs())
#lapply(list.dirs(), rtoz)
