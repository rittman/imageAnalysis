aa <- read.table("cloud.txt")
bb <- read.table("cloud_fit.txt", na.string="NaN")

bb[,1] <- bb[,1]
aa[,1] <- aa[,1]


ylimit=max(abs(aa[,2]), na.rm=TRUE)

jpeg(filename="cloud.jpg", width=400, height=400, quality=100)
plot(NA,NA, ylim=c(-ylimit,ylimit), xlim=c(0,180), ylab="delta R", xlab="Euclidean Distance (mm)")

points(aa[,1], aa[,2], pch=16, cex=0.5, col="blue")
lines(bb[complete.cases(bb),], col="red")
abline(0,0, col="red")
dev.off()
