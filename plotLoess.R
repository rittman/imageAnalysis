plotPoints <- function(y, x){
	points(x,y, pch=16, cex=0.5)
}

aa <- read.table("loess.txt")
bb <- read.table("functional_reordered_pp_wpd_MNI500_ts_col_dbold.txt")
cc <- scan("functional_reordered_motion_fd.txt")

maxx <- max(cc, na.rm=TRUE)
maxy <- max(bb, na.rm=TRUE)

jpeg(filename="loess.jpg", width=400, height=400, quality=100)
plot(x=NA, y=NA, xlim=c(0,maxx), ylim=c(0,maxy), ylab="|d%BOLDx10|", xlab="Framewise Displacement (mm)")
apply(bb, 2, plotPoints, x=cc)
lines(aa, col="red")

dev.off()
