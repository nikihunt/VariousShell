手动添加jar包到maven本地仓库

1、几个好的 Maven 常用仓库网址：
http://mvnrepository.com/
http://search.maven.org/
http://repository.sonatype.org/content/groups/public/
http://people.apache.org/repo/m2-snapshot-repository/
http://people.apache.org/repo/m2-incubating-repository/

2、去上面的几个常用仓库中搜索要找的jar包并下载到本地，同时要记得这个 jar 包的 groupId，artifactId，version信息

3、用maven命令安装jar包到本地仓库：
mvn install:install-file -Dfile=jar包的位置 -DgroupId=上面的groupId -DartifactId=上面的artifactId -Dversion=上面的version -Dpackaging=jar