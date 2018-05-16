x = c(1,3,5,7,9)
xmean = mean(x)

f = file("testR.txt")
writelines(xmean,f)
close(f)
