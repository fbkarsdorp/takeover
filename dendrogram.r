library(ggplot2)
library(ggdendro)
library(FNN)

# read the topic matrix
atm = read.csv("~/Dropbox/TIME/ATM/atm.csv", header=T, sep=",")
# compute KL divergence into distance matrix
atm.kl = KLdiv(as.matrix(t(atm)))
# cluster names using ward clustering
atm.clust = hclust(as.dist(atm.kl), method="ward")
names = read.table("~/Dropbox/TIME/ATM/atm_categories.txt", header=T, sep=",")
hcdata = dendro_data(atm.clust)
hcdata$labels = merge(x=hcdata$labels, y=names, by.x="label", by.y="PERSON")

ggplot() + geom_segment(data=segment(hcdata), 
	                    aes(x=x, y=y, xend=xend, yend=yend)) + 
  geom_text(data=label(hcdata), 
	      aes(x=x, y=y, label=label, colour=CATEGORY, hjust=0), size=2) + 
  coord_flip() + scale_y_reverse(expand=c(0.2, 0)) + 
  scale_colour_brewer(palette="Dark2") + 
  theme(panel.background = element_rect(fill="#DDE3CA"), 
  	    panel.grid.major=element_blank(), 
  	    panel.grid.minor=element_blank(), 
  	    legend.position = "top", 
  	    panel.margin=unit(x=c(0, 0, 0, 0), units="mm"), 
  	    plot.background=element_rect(fill="#DDE3CA"), 
  	    legend.background=element_rect(fill="#DDE3CA"), 
  	    axis.text=element_blank(), axis.ticks=element_blank()) + 
  xlab("") + 
  ylab("")