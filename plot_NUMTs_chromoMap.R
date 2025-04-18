install.packages("chromoMap")
# install.packages("chromoMap")
library(chromoMap)
library(colorBlindness)
library(RColorBrewer)

# Get the number of unique categories in the last column of the annotation file
n_colors <- length(unique(annot_file_win_5000K[[ncol(annot_file_win_5000K)]]))
data_colors <- list(colorRampPalette(brewer.pal(9, "Set3"))(n_colors))

# Reference: https://cran.r-project.org/web/packages/chromoMap/vignettes/chromoMap.html#My_first_chromoMap

# Base directory path (optional if using absolute paths later)
base_path <- "C:/Users/THOMAS CLAVIJO/Documents/Tesis/Articulo final ludens/Articulo final/cromoMap"

# Set working directory
setwd(base_path)

# Load input files
chr_new_file <- read.table("chromosome_file.txt", sep = '\t', header = FALSE)
annot_file <- read.table("resultado_blastn.txt", sep = '\t', header = FALSE)
annot_file_win_5000K <- read.table("resultado_blastn_editado_cromomap.txt", sep = '\t', header = FALSE)

# Check the number of categories
table(annot_file_win_5000K[[ncol(annot_file_win_5000K)]])

# Automatically generate a color palette with 20 colors
n_colors <- length(unique(annot_file_win_5000K[[ncol(annot_file_win_5000K)]]))
color_palette <- colorRampPalette(brewer.pal(9, "Set3"))(n_colors)

# Create the plot
plot_chr <- chromoMap(
  list(chr_new_file),
  list(annot_file_win_5000K),
  data_based_color_map = TRUE,
  data_type = "categorical",
  fixed.window = TRUE,
  window.size = 500000,
  win.summary.display = TRUE,
  data_colors = list(color_palette),
  left_margin = 80,
  interactivity = FALSE
)

# Display the plot
plot_chr
