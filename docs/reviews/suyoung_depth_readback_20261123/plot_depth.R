args <- commandArgs(trailingOnly = TRUE)
d <- read.csv(args[1], check.names = FALSE)
a <- d[d$F12_step == as.integer(args[3]),]
b <- d[d$F12_step == as.integer(args[4]),]
png(args[2], width = 1800, height = 1200, res = 163)
par(family = "sans", bty = "n", las = 1, lend = "round", xaxs = "i", yaxs = "i",
    col.axis = "#344958", col = "#1D3341", tcl = -.24)
labels <- c("Lower third", "Middle third", "Upper third", "Total")
keys <- c("lower", "middle", "upper", "whole")
colors <- c("#B54723", "#147195", "#577940", "#253746")
axis_color <- "#7C8B96"
layout(matrix(1:2,ncol = 1), heights = c(1.25, 1))
par(mar=c(4.2,4.8,5.7,1.3))
plot(NA, xlim=c(0,.085),ylim=c(-.043,.098), axes=FALSE,xlab="",ylab="")
yt <- seq(-.04,.08,.02)
abline(h=yt,col="#DFE6EA",lwd=.65)
abline(h=0,col=axis_color,lwd=1)
abline(v=c(a$travel_D,b$travel_D),col="#94A2AD",lty=3,lwd=1.5)
axis(1,at=seq(0,.08,.01),labels=sprintf("%.2f",seq(0,.08,.01)),col=axis_color,col.ticks=axis_color)
axis(2,at=yt,labels=sprintf("%.2f",yt),col=axis_color,col.ticks=axis_color)
for(k in 1:4) lines(d$travel_D,d[[keys[k]]],col=colors[k],lwd=if(k==4) 2.0 else 1.7,lty=if(k==4) 5 else 1)
text(a$travel_D,.092,"A",font=2,cex=.95)
text(b$travel_D,.092,"B",font=2,cex=.95)
mtext("Plate travel / particle diameter",1,line=2.55,cex=.98)
mtext("Difference in vertical momentum change rate (MPa equivalent)",3,line=.55,adj=0,font=2,cex=.99)
mtext("Layer contributions to the F12 minus F24 difference",3,line=3.75,adj=0,font=2,cex=1.57)
mtext("Half-speed loading  |  Material points grouped by their initial depth",3,line=2.12,adj=0,cex=1.02,col="#49606E")
legend("topleft",labels,col=colors,lty=c(1,1,1,5),lwd=c(1.7,1.7,1.7,2),ncol=2,bty="n",cex=.9,
       inset=c(.006,.01),x.intersp=.6,y.intersp=1.06)

par(mar=c(2.1,4.8,3.45,1.3))
plot(NA,xlim=c(0.36,9.64),ylim=c(-.021,.104),axes=FALSE,xlab="",ylab="")
yt <- seq(-.02,.08,.02)
abline(h=yt,col="#DFE6EA",lwd=.65)
abline(h=0,col=axis_color,lwd=1)
axis(2,at=yt,labels=sprintf("%.2f",yt),col=axis_color,col.ticks=axis_color)
x1 <- 1:4
x2 <- 6:9
axis(1,at=c(x1,x2),labels=rep(c("Lower","Middle","Upper","Total"),2),col=axis_color,col.ticks=NA,cex.axis=.9)
for(i in 1:4) {
  for(pair in list(list(x1[i],a),list(x2[i],b))) {
    value <- pair[[2]][[keys[i]]]
    xpos <- pair[[1]]
    segments(xpos,0,xpos,value,col=colors[i],lwd=2.7)
    points(xpos,value,pch=21,bg=colors[i],col="white",lwd=1.2,cex=1.22)
    text(xpos,value + if(value>=0) .005 else -.0037, sprintf("%+.4f",value),col=colors[i],font=2,cex=.85)
  }
}
mtext("At the two bottom-pressure gap landmarks (MPa equivalent)",3,line=1.98,adj=0,font=2,cex=1.04)
text(mean(x1),.097,sprintf("A   First common step above 5%%  |  %.5f D",a$travel_D),font=2,cex=.88)
text(mean(x2),.097,sprintf("B   Peak pressure gap  |  %.5f D",b$travel_D),font=2,cex=.88)
invisible(dev.off())
