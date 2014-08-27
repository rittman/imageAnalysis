library(car)
aa <- read.table("FDcorrConnVsDistance.txt", na.string="NaN")

jpeg(filename="satterthwaite.jpg", width=1200, height=1200, quality=100, pointsize=12, res=300)
names(aa) <- c("Distance", "Value")
scatterplot(Value~Distance,
				data=aa,
				pch=16, 
				cex=0.5, 
				xlab="Inter-Node Euclidean Distance (mm)", 
				ylab="Correlation of Motion and Connectivity (r)",
				ylim=c(-0.8, 0.8))
sink("SatterthwaiteCorrelationsLog.txt")
cor.test(aa[complete.cases(aa[,2]),1],aa[complete.cases(aa[,2]),2], method="pearson")
sink()
dev.off()