args <- commandArgs(trailingOnly = TRUE)
series <- read.csv(args[1], na.strings = "")
series <- subset(series, turns >= 0)
png(args[2], width = 1800, height = 1120, res = 166, bg = "white")
par(mfrow = c(2, 1), mar = c(3.3, 5.2, 2, 1.1), oma = c(1.6, .5, 3.8, .2),
    las = 1, bty = "l", family = "sans", cex.axis = 1.1, cex.lab = 1.1)
panel <- function(y, label, color) {
    valid <- is.finite(y)
    limits <- if (any(valid)) range(c(0, y[valid])) else c(0, 1)
    if (diff(limits) <= 0) limits <- limits + c(-.02, .02)
    plot(NA, xlim = c(0, 2.02), ylim = limits, xaxs = "i", xlab = "", ylab = label)
    usr <- par("usr")
    rect(1, usr[3], 2, usr[4], col = "#eff4f5", border = NA)
    abline(v = 1, lty = 3, col = "#819096")
    if (any(valid)) {
        lines(series$turns, y, col = color, lwd = 1.8)
        points(series$turns[valid], y[valid], col = color, pch = 16, cex = .28)
    }
    if (any(!valid)) rug(series$turns[!valid], ticksize = .035, col = "#a94615")
}
panel(series$theta_abs_deg, "Surface angle (degrees)", "#136b73")
if (length(args) >= 3) {
    secondary <- read.csv(args[3], na.strings = "")
    lines(secondary$turns, abs(secondary$dense_signed_deg), col = "#a25c15", lwd = 1.4)
    legend("topright", c("Upper particle envelope", "Occupied bed edge"),
           col = c("#136b73", "#a25c15"), lty = 1, lwd = 2, bty = "n",
           horiz = TRUE, cex = .83)
}
panel(series$delta_over_R, "Layer thickness / drum radius", "#61427a")
mtext("Completed drum turns", side = 1, line = 2.35)
mtext("B2-U   |   Free surface and flowing layer", side = 3, outer = TRUE, line = 1.75,
      adj = .04, font = 2, cex = 1.42, col = "#19282f")
mtext("One seed at 76.68 rpm. Shaded interval: second turn. Rust ticks: unresolved frames.",
      side = 3, outer = TRUE, line = .2, adj = .04, col = "#465963")
dev.off()
