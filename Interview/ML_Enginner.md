## Machine Learning-Related Questions

> The biggest difference is that unsupervised learning does not require explicitly labeled data, while supervised learning does – before you can do a classification, you must label the data to train the model to classify data into the correct groups.

#### 1. What are the different types of machine learning?

- 监督学习；通过大量带有标记的数据来训练机器，机器将预测结果与期望结果进行比对；之后根据比对结果来修改模型中的参数，再一次输出预测结果；然后将预测结果与期望结果进行比对，重复多次直至收敛，最终生成具有一定鲁棒性的模型来达到智能决策的能力。
- 无监督学习；机器从无标记的数据中探索并推断出潜在的联系。常见的有聚类和降维。
- 强化学习；一种对机器的行为带有激励机制的学习，具体来说，如果机器行动正确，将施予一定的“正激励”；如果行动错误，同样会给出一个惩罚。
- 深度学习；建立人工的神经网络，通过不断组合低层特征，形成更加抽象的高层属性类别或特征；应用：计算机视觉，语音识别，自然语言处理等。

#### 2. What is deep learning, and how does it contrast with other machine learning algorithms?

Deep Learning 是一种特殊的机器学习，其中深度的意思是很多连续的层，一个模型的深度也就是表示这个模型有多少层。


#### 3. What are the differences between machine learning and deep learning?

- Deep learning 机器学习的分支.
- 算法学习方式不一样，需要的数据量不一样
- Deep learning 自动提取特征，比较擅长处理非结构化数据，机器学习则一般要求结构化的数据

>[AI vs. Machine Learning vs. Deep Learning vs. Neural Networks](https://www.ibm.com/cloud/blog/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks)



#### 4. Explain the confusion matrix with respect to machine learning algorithms.

Confusion Matrix这个概念告诉我们，机器学习的算法预测的结果中，正确了多少、错了多少以及正确的分布在哪里，错的又分布在哪里。

通过这个模型，我们可以来衡量不同模型的效果，选择一个最好的模型。

#### 5. What is the difference between artificial intelligence and machine learning?

AI is a bigger concept to create intelligent machines that can simulate human thinking capability and behavior, whereas, machine learning is an application or subset of AI that allows machines to learn from data without being programmed explicitly.


#### 6. What’s the trade-off between bias and variance?

bias高，可以理解为反应慢，但很稳。而Variance高，则意味反应很灵敏，发挥可能有时候很好，有时候很差。

直线的Variance比较低，因为对于不同的数据集的预测结果，算出来的最小二乘法之和比较低。

另外一种机器学习的描述方式，虽然我们的曲线模型对与训练数据fit的非常完美，但是在测试数据中却不理想，我们说这个模型overfit了。

理想的模型是variance和bias都比较低，能准确的反映数据的分布关系，以及做出稳定的预测。


#### 7. Explain the difference between L1 and L2 regularization.

L1 Regularization, also called a lasso regression, adds the “absolute value of magnitude” of the coefficient as a penalty term to the loss function.

Lasson回归的特点是，它可以自己选择feature，这样就会把那些不重要features的系数降为或者说（shrink）为0.

当我们训练好模型后，我们可以通过 .coef_ 来查看模型中各个features的权重，或者说偏好。


L2 Regularization, also called a ridge regression, adds the “squared magnitude” of the coefficient as the penalty term to the loss function.

ridge regression就是一个加强版的OLS loss function，它多了一个阿尔法参数，当阿尔法为0的时候，ridge regression变成了普通的ols函数，当阿尔法变得很大，对overfitting的惩罚也变得更大，更敏感，这会让模型变得过于简单(underfitting).

对于ridge regression的使用，它多了个alpha参数。另外对于不同参数，我们需要将它 归一化，所以在初始化ridge实例的时候，需要指定 normalize=true.


#### 8. What’s your favorite algorithm, and can you explain it to me in less than a minute?

KNN. 它是广为使用的一种机器学习算法，理论上比较成熟的方法，也是最简单的机器学习算法。当时我拿 jira 的 ticket 训练处理 ticket 请求的分类问题。


#### 9. How is KNN different from k-means clustering?

KNN represents a supervised classification algorithm that will give new data points accordingly to the k number or the closest data points,

while k-means clustering is an unsupervised clustering algorithm that gathers and groups data into k number of clusters.

#### 10. What is cross validation and what are different methods of using it?

Cross Validation 可以让我们大概知道哪些模型会fit比较好，哪些模型在实际应用的时候表现会更好. 逐一将所有的数据都测试一遍，然后汇总结果。这样每一组数据都作为测试数据参与过模型训练，也参与过模型的检测。逐一测试后，再汇总所有结果，我们就可以选择最适合数据的模型。

#### 11. Explain how a ROC curve works.

- Sensitivity， 所有肥胖的老鼠中，多少预测对了；
- Specificity，所有没有肥胖的老鼠中，多少预测对了；
- ROC，Sensitivity X轴、Specificity Y 轴;

#### 12. What’s the difference between probability and likelihood?

- Probabiity（概率）：给定某一参数值，求某一结果的可能性

- Likelihood（似然）：给定某一结果，求某一参数值的可能性


#### 13. What’s the difference between a generative and discriminative model?

判别式模型举例：要确定一个羊是山羊还是绵羊，用判别模型的方法是从历史数据中学习到模型，然后通过提取这只羊的特征来预测出这只羊是山羊的概率，是绵羊的概率。生成式模型举例：利用生成模型是根据山羊的特征首先学习出一个山羊的模型，然后根据绵羊的特征学习出一个绵羊的模型，然后从这只羊中提取特征，放到山羊模型中看概率是多少，在放到绵羊模型中看概率是多少，哪个大就是哪个。

链接：https://www.zhihu.com/question/20446337/answer/256466823


#### 14. How is a decision tree pruned?

当训练数据量大、特征数量较多时构建的决策树可能很庞大，这样的决策树用来分类是否好？答案是否定的。

决策树是依据训练集进行构建的，为了尽可能正确地分类训练样本，结点划分过程将不断重复，有时会造成决策树分支过多。这就可能会把训练样本学的“太好”了，以至于把训练集自身的一些特点当作所有数据都具有的一般性质而导致过拟合。因此可主动去掉一些分支来降低过拟合风险。

决策树非常容易产生过拟合，实际所有非参数学习算法，都非常容易产生过拟合。

因此，对于决策树的构建还需要最后一步，即决策树的修剪。两个目的：降低复杂度，解决过拟合。

决策树的修剪，也就是剪枝操作，主要分为两种：

预剪枝（Pre-Pruning）
后剪枝（Post-Pruning）

[参考](https://cloud.tencent.com/developer/article/1558404)

#### 15. How can you choose a classifier based on a training set size?

首先搞清楚 bias 和 variance 两个概念：

bias高，可以理解为反应慢，但很稳。而Variance高，则意味反应很灵敏，发挥可能有时候很好，有时候很差。


If the training set is small, high bias / low variance models (e.g. Naive Bayes) tend to perform better because they are less likely to overfit.

If the training set is large, low bias / high variance models (e.g. Logistic Regression) tend to perform better because they can reflect more complex relationships.

#### 16. What methods for dimensionality reduction do you know and how do they compare with each other?

参考：[12种降维方法终极指南（含Python代码）](https://zhuanlan.zhihu.com/p/43225794)

#### 17. Define precision and recall.

假设一共有10篇文章，里面4篇是你要找的。根据你某个算法，你认为其中有5篇是你要找的，但是实际上在这5篇里面，只有3篇是真正你要找的。那么你的这个算法的precision是3/5=60%，也就是，你找的这5篇，有3篇是真正对的这个算法的recall是3/4=75%，也就是，一共有用的这4篇里面，你找到了其中三篇。

链接：https://www.zhihu.com/question/19645541/answer/12502751


#### 18. What’s a Fourier transform?

一种将原来空间中难以处理的问题变换到方便计算的空间中去，比如在修图技术中，将 RGB 信息做变换；在音频处理中，将低频或者高频等部分分离出来。

#### 19. What’s the difference between Type I and Type II error?

(Type I error)，原假设是正确的，而你判断它为错误的；
(Type II error)，原假设是错误的，而你判断它为正确的。 我们分别称这两种错误为第一类错误和第二类错误 。


#### 20. When should you use classification over regression?

Classification is about identifying group membership while regression technique involves predicting a response.

 Both techniques are related to prediction, where classification predicts the belonging to a class whereas regression predicts the value from a continuous set.

 Classification technique is preferred over regression when the results of the model need to return the belongingness of data points in a dataset to specific explicit categories. (For instance, when you want to find out whether a name is male or female instead of just finding it how correlated they are with male and female names.


#### 21. How would you evaluate a logistic regression model?

如果利用逻辑回归来解决分类问题，那么可以使用 AUC, Confusion Matrix.
如果利用它解决线性回归问题（比如想知道各种变量之间的关系）那么可以查看 odds ratios 和 standard errors，或者是R方。

没有一种完美的方法，因为这还取决于模型的假设。

#### 22. What is Bayes’ Theorem? How is it useful in a machine learning context?

用来计算某一事件(E)已经发生(例如在测试中被诊断为阳性)时假设(H)为真的概率。


#### 23. Describe a hash table.

哈希表，通过键来访问值的一种数据结构，从键到值得这种关系成为映射关系，哈希函数可能会发生碰撞，这时候需要通过链表来解决。

## Technical Skills Questions

> The company will want to make sure you have the hard skills needed to excel in the Machine Learning Engineer position. For technical questions, remember that interviewers are usually more interested in your thought process than the final solution.


#### 24. How would you handle an imbalanced dataset?

1. 使用正确的模型衡量标准，比如 AUC，F1 Score 等来查看模型是否可以 apply.
2. 对数据重采样。欠采样，针对数据特征比较丰富；重采样：针对数据质量比较差的情况
3. 使用 k-fold cross-validation
4. 继承不同的重采样数据
5. 按照不同比例重采样



#### 25. How do you handle missing or corrupted data in a dataset?

1. 如果这些值随机出现，或者移除后对整体的体量没有什么影响，直接删除相关的列与行
2. 将缺失的值填充成聚合后的值
3. 创建一个 unknow 的组，将这些值放进去
4. 预测这些缺失的值

#### 26. Do you have experience with Spark or big data tools for machine learning?

有，使用 Spark 来处理大的数据集。

#### 27. Pick an algorithm. Write the pseudo-code for a parallel implementation.

省略。

#### 28. Which data visualization libraries do you use? What are your thoughts on the best data visualization tools?

画图：

- Plotly.
- seaborn

web:
- Dash
- Streamlit
- Metabase

#### 29. Given two strings, A and B, of the same length n, find whether it is possible to cut both strings at a common point such that the first part of A and the second part of B form a palindrome.

省略。

#### 30. How would you build a data pipeline?

定义 data pipline, An ETL pipeline is the sequence of processes that move data from a source (or several sources) into a database, such as a data warehouse. 

- 部署 pip line 工具，比如 airflow 和 Luigi
- 直接使用 pandas 手写


#### 31. How would you implement a recommendation system for our company’s users?

推荐系统的分类，有三种：

1. 基于人口的统计学推荐(Demographic-based
2. 基于内容的推荐(Content-based Recommendation)，根据物品或内容的元数据，发现物品或内容的相关性，然后基于用户以前的喜好记录推荐给用户相似的物品。
3. 基于协同过滤的推荐(Collaborative Filtering-based Recommendation)

[参考](https://www.zhihu.com/question/19971859)

#### 32. Can you explain your approach to optimizing auto-tagging?

省略。

#### 33. Suppose you are given a data set that has missing values spread along 1 standard deviation from the median. What percentage of data would remain unaffected and why?

省略。

#### 34. Suppose you found that your model is suffering from low bias and high variance. Which algorithm do you think could tackle this situation and why?

- By minimizing the total error
- Using Bagging and Resampling techniques
- djusting minor values in algorithms
- using a proper Machine learning workflow


#### 35. You are given a data set. The data set contains many variables, some of which are highly correlated and you know about it. Your manager has asked you to run PCA. Would you remove correlated variables first? Why?

参考[Should one remove highly correlated variables before doing PCA?](https://stats.stackexchange.com/questions/50537/should-one-remove-highly-correlated-variables-before-doing-pca)


#### 37. What are the advantages and disadvantages of neural networks?

优点:
- 分类的准确度高；
- 并行分布处理能力强,分布存储及学习能力强，
- 对噪声神经有较强的鲁棒性和容错能力，能充分逼近复杂的非线性关系；
- 具备联想记忆的功能。

缺点:

- 神经网络需要大量的参数，如网络拓扑结构、权值和阈值的初始值；
- 不能观察之间的学习过程，输出结果难以解释，会影响到结果的可信度和可接受程度；
- 学习时间过长,甚至可能达不到学习的目的。

#### 38. How would you go about understanding the sorts of mistakes an algorithm makes?

省略。

#### 39. Explain the steps involved in making decision trees.

省略。

## Personal Questions

> In addition to your experience in machine learning, employers are looking for candidates with passion, enthusiasm, and the right personality. Personal questions help interviewers get to know more about you, your work style, and your interests.

#### 40. How do you keep informed of developments in machine learning?



#### 41. How do you think quantum computing will affect machine learning?



#### 42. Is machine learning a science or an art?



#### 43. What are you passionate about?



#### 44. How do you handle stress and pressure?



#### 45. What makes you unique?



#### 46. What motivates you?



#### 47. Tell me about yourself.



#### 48. How would you describe yourself?



#### 49. How do you evaluate success?



#### 50. What is your greatest weakness?



#### 51. What is your greatest strength?



#### 52. Describe your work ethic.



#### 53. Why do you want to work here?


## Leadership and Communication

> As a Machine Learning, you may be expected to lead projects and interact with technical and non-technical team members and clients. Expect questions that test essential leadership and communication skills. Examples of leadership and communication interview questions include:



#### 54. Tell me about a time when you had to convince others to take your position on a specific matter. What was the outcome?



#### 55. How do you make sure projects and tasks stay on schedule?



#### 56. How do you handle disagreements on your team?



#### 57. Tell me about a time when something went wrong at work and you took control.



#### 58. How do you deal with people who disagree with you?



#### 59. How would you go about simplifying a complex issue in order to explain it to a client or colleague?



#### 60. How would you go about persuading someone to see things your way at work?



#### 61. How would you go about explaining a complex idea/problem to a client who was already frustrated?



#### 62. What would you do if there was a breakdown in communication at work?



#### 63. Talk about a successful presentation you gave and why you think it did well.



#### 64. Talk about a time when you made a point that you knew your colleagues would be resistant to.



#### 65. Is it more important to be a good listener or a good communicator?


## Behavioral

> To successfully answer a behavioral question, start by outlining the situation, then explain your responsibilities, describe the steps you took, and, finally, share the outcomes of your actions. Examples of behavioral interview questions include:


#### 66. Give me an example of how you’ve used your data analysis to change behavior. What was the impact, and what would you do differently in retrospect?



#### 67. Give an example of a problem you solved (or tried to solve) with machine learning.



#### 68. Tell me about a time when you had to think outside the box to complete a task. Were you successful?



#### 69. Can you describe a time when you had to develop a complex algorithm?



#### 70. Can you tell me about a major success you had with a machine learning project?



#### 71. What’s the most difficult decision you’ve had to make recently and how did you come to that decision?



#### 72. Tell me about a time you were under a lot of pressure. What was going on, and how did you get through it?



#### 73. Tell me about a time you had a conflict at work.



#### 74. Give an example of when you made a mistake at work.



#### 75. Describe a time when you disagreed with a client. How did you handle it?



#### 76. Tell me about a time you set a goal for yourself. How did you go about ensuring that you would meet your objective?



#### 77. Describe a time when you saw a problem and took the initiative to correct it rather than waiting for someone else to do it.


## Questions From Top Companies

> Wondering what top tech companies are looking for in Machine Learning Engineers? Here are a few interview questions from Amazon, Google, Facebook, and Microsoft.


#### 78. What are the differences between generative and discriminative models?



#### 79. How would you weigh nine marbles three times on a balance scale to select the heaviest one?



#### 80. What’s the difference between MLE and MAP inference?



#### 81. Why did you use this particular machine learning algorithm in your project?



#### 82. What is K-means algorithm?



#### 83. Describe a time when you let go of a short-term goal for a long-term goal.



#### 84. What’s the difference between the summaries of a Logistic Regression and SVM?



#### 85. Explain ICA and CCA. How do you get a CCA objective function from PCA?



#### 86. What is the relationship between PCA with a polynomial kernel and a single layer autoencoder? What if it is a deep autoencoder?



#### 87. What is A/B testing in machine learning?



#### 88. What is activation function in machine learning?



#### 89. How would you build, train and deploy a system to detect if multimedia and/or ad content being posted violated terms or contained offensive materials?



#### 90. How do you solve a disagreement with a team member?



#### 91. What is the bias-variance tradeoff? How is it expressed using an equation?



#### 92. Describe the idea behind boosting. Give an example of one method and describe one advantage and disadvantage.



#### 93. Formulate the background behind an SVM, and show the optimization problem it aims to solve.


