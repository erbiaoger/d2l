# 指定矩阵的行数和列数
rows <- 3
cols <- 4

# 使用runif()函数生成均匀分布的随机数矩阵
random_matrix <- matrix(runif(rows * cols), nrow = rows, ncol = cols)

# 打印随机矩阵
print(random_matrix)

# 绘制热力图
heatmap(random_matrix, 
        col = colorRampPalette(c("blue", "white", "red"))(100),  # 颜色范围
        main = "随机矩阵热力图",  # 主标题
        xlab = "列",  # X轴标签
        ylab = "行"   # Y轴标签
)

# 保存图像为PNG文件
png("heatmap.png", width = 800, height = 600)  # 设置图像大小
# dev.off()  # 关闭设备并保存图像