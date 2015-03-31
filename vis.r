require('ggplot2')
res = read.csv("results.csv", header=FALSE)
res = mutate(res, Percent = 100*(V2/(sum(res$V2))))
ggplot(data=res, aes(x=V1, y=V2, fill=Percent)) + geom_bar(stat="identity") + coord_flip() + xlab('Facility') + ylab('Number Of Violations')