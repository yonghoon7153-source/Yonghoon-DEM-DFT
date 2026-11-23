args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Expected settings TSV and output PNG.")
review <- read.delim(args[1], check.names = FALSE, na.strings = "", stringsAsFactors = FALSE)
cells <- c(8, 12, 16, 24)
columns <- paste0("phi_m_", cells)
stopifnot(identical(review$setting, 1:4),
          sum(!is.na(as.matrix(review[columns]))) == 4L)
phi <- unlist(review[review$setting == 1L, columns], use.names = FALSE)
delta <- abs(phi[2] - phi[3])
stopifnot(all(is.finite(phi)), abs(delta - review$abs_delta_12_16[1]) < 2e-12,
          delta > 0.005, identical(review$u6a[1], "FAIL"))

ink <- "#182E3C"
secondary <- "#445A64"
blue <- "#255E74"
orange <- "#AA4725"
png(args[2], width = 2240, height = 1440, res = 180, bg = "white",
    pointsize = 18)
par(mai = c(1.63, 1.46, 1.68, .56), family = "sans", fg = ink,
    col.axis = secondary, col.lab = ink, lend = "round", xaxs = "i",
    yaxs = "i", mgp = c(2.72, .73, 0), tcl = -.21)
plot.new()
plot.window(xlim = c(7, 25.1), ylim = c(.930, 1.016))
ticks <- c(.94, .96, .98, 1)
abline(h = ticks, col = "#E1E8EA", lwd = 1.15)
axis(1, at = cells, labels = cells, lwd = 1.3, cex.axis = 1.04)
axis(2, at = ticks, labels = sprintf("%.2f", ticks), las = 1,
     lwd = 1.3, cex.axis = 1.04)
mtext("Grid cells per particle diameter", side = 1, line = 2.35, cex = 1.05)
mtext(expression(paste("Reference-area fraction, ", italic(Phi)[m])),
      side = 2, line = 3.12, cex = 1.05)
mtext("Setting 1 misses the grid agreement limit", side = 3,
      line = 3.01, adj = 0, font = 2, cex = 1.43, col = ink)
mtext("Solid fraction at the first 1.2 MPa crossing of the bottom-plate pressure",
      side = 3, line = 1.14, adj = 0, cex = .94, col = secondary)

lines(cells, phi, lwd = 2.1, col = "#879BA1")
lines(cells[2:3], phi[2:3], lwd = 3.0, col = orange)
points(cells, phi, pch = 21, cex = 1.49, bg = c(blue, orange, orange, blue),
       col = "white", lwd = 1.7)
text(cells, phi + .0040, sprintf("%.5f", phi), col = c(blue, orange, orange, blue),
     cex = .95, font = 2)

segments(16.05, phi[3] - .0010, 16.95, .973, col = "#BAA9A0", lwd = 1.2)
text(17.20, .970, "12 vs 16 cells", adj = 0, cex = 1.04, font = 2, col = ink)
text(17.20, .9623, sprintf("Difference  %.6f", delta),
     adj = 0, cex = 1.04, col = orange, font = 2)
text(17.20, .9548, expression(paste("Pass limit  ", "" <= " 0.005")),
     adj = 0, cex = .96, col = secondary)
mtext("Development data, 23 Nov 2026. Settings 2-4 have no measured values.",
      side = 1, line = 4.05, adj = 0, cex = .78, col = secondary)
invisible(dev.off())
