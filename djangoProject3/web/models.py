from django.db import models

#cjy开始
class Studentlogin(models.Model):
    ID = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name='身份编号')
    password = models.CharField(max_length=12, default='student', verbose_name="密码")

class Mishulogin(models.Model):
    ID = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name='身份编号')
    password = models.CharField(max_length=12, default='student', verbose_name="密码")

class Applicant(models.Model):
    StudentID = models.CharField(max_length=100, unique=True, verbose_name="考生编号", primary_key=True)
    EnglishScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="英语成绩")
    MathScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="数学成绩")
    PoliticScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="政治成绩")
    MajorScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="专业课成绩")

    def __str__(self):
        return self.StudentID

    class Meta:
        verbose_name = "考生志愿信息"
        verbose_name_plural = "考生志愿信息"


class StudentTotalScore(models.Model):
    StudentID= models.CharField(max_length=100,primary_key=True,unique=True,verbose_name="考生编号")
    program_name = models.CharField(max_length=255,verbose_name="学生方向",null=True)
    total_score = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    rank = models.IntegerField(null=True,verbose_name="排名")
    is_admitted = models.IntegerField(default=0)

    def __str__(self):
        return self.StudentID

class ExamResult(models.Model):
    StudentID = models.CharField(max_length=100, unique=True, verbose_name="考生编号", primary_key=True)
    WrittenExamScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="考生编号")
    InterviewScore = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="面试成绩")
    isadmitted =models.CharField(max_length=10, null=True, verbose_name="是否录取")

    def __str__(self):
        return self.StudentID

    class Meta:
        verbose_name = "考生复试信息"
        verbose_name_plural = "考生复试信息"

#cjy结束

#lyy开始
class TeacherInfo(models.Model):
    TeacherID = models.CharField(max_length=10, unique=True, primary_key=True,verbose_name='导师编号')
    password=models.CharField(max_length=12, default='bjfuteacher',verbose_name="密码")
    Name = models.CharField(max_length=50, verbose_name='邮箱')
    Title = models.CharField(max_length=50, verbose_name='职称',null=True)
    Photo = models.ImageField(upload_to='teacher_photo/', verbose_name='导师个人照', null=True, blank=True)
    Biography = models.TextField(verbose_name='个人简介',null=True)
    Email=models.EmailField(max_length=100,verbose_name='邮箱',null=True)
    Phone=models.CharField(max_length=11,verbose_name='电话',null=True)
    AcademicAchievements=models.TextField(max_length=100,verbose_name="学术成就",null=True)
    EnrollmentQuota=models.IntegerField(verbose_name="招生指标",null=True,default=0)
    Selected = models.IntegerField(verbose_name="选了多少学生",default=0)
    QualificationReview = models.IntegerField(verbose_name="资格审查",default=0,null=True)


class StudentInfo(models.Model):
    studentId=models.CharField(max_length=10,unique=True, primary_key=True,verbose_name='学生编号')
    name=models.CharField(max_length=100,verbose_name='学生姓名')
    gender=models.CharField(max_length=10,verbose_name='性别')
    school=models.CharField(max_length=100,verbose_name='本科学校')
    major=models.CharField(max_length=100,verbose_name='本科专业')
    phone=models.CharField(max_length=15,verbose_name='电话')
    direction=models.CharField(max_length=100,verbose_name='专业方向')
    isadmitted=models.CharField(max_length=10,verbose_name='是否录取',null=True,blank=True)
    FirstChoice = models.CharField(max_length=10, null=True,blank=True,verbose_name='第一志愿的导师编号')
    SecondChoice = models.CharField(max_length=10, null=True,blank=True,verbose_name='第二志愿的导师编号')
    ThirdChoice = models.CharField(max_length=10, null=True,blank=True,verbose_name='第三志愿的导师编号')
    FinalTeacher = models.ForeignKey(
        TeacherInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='FinalTeacher',
        verbose_name='最终的导师'
    )
    stage=models.IntegerField(verbose_name="第几阶段被选",null=True,blank=True)

class OtherInfo(models.Model):
    ID = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name='身份编号')
    password = models.CharField(max_length=12, default='bjfuworker', verbose_name="密码")

class MissedTeacher(models.Model):
    TeacherID = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name='导师编号')
    Name = models.CharField(max_length=50, verbose_name='名字')
    begin=models.DateTimeField(verbose_name="补选开始时间",null=True)
    end=models.DateTimeField(verbose_name="补选结束时间", null=True)

class StageTime(models.Model):
    ID=models.AutoField(primary_key=True, verbose_name='编号')
    Fbegin=models.DateTimeField(verbose_name="第一阶段开始日期")
    Fend = models.DateTimeField(verbose_name="第一阶段结束日期")
    Sbegin=models.DateTimeField(verbose_name="第一阶段开始日期")
    Send=models.DateTimeField(verbose_name="第一阶段结束日期")
    Tbegin=models.DateTimeField(verbose_name="第一阶段开始日期")
    Tend=models.DateTimeField(verbose_name="第一阶段结束日期")


class AdditionStageTime(models.Model):
    TeacherID=models.CharField(max_length=10, unique=True, primary_key=True,verbose_name='导师编号')  #人工选出来的 会变化
    Name = models.CharField(max_length=50, verbose_name='名字')
    Rest=models.IntegerField(verbose_name='缺额数量')
    Abegin=models.DateTimeField(verbose_name="补选开始时间",null=True)
    Aend=models.DateTimeField(verbose_name="补选结束时间",null=True)
#lyy结束


#wjx开始
class XueKelogin(models.Model):
    ID = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name='身份编号')
    password = models.CharField(max_length=12, default='student', verbose_name="密码")

class College(models.Model):
    """学院表"""
    college_id = models.CharField(max_length=10, verbose_name="学院ID", primary_key=True)
    college_name = models.CharField(max_length=100, verbose_name="学院名称")
    total_recruit = models.IntegerField(default=0, verbose_name="总招生人数")

    def __str__(self):
        return f"{self.college_name} ({self.college_id})"

    class Meta:
        verbose_name = "学院"
        verbose_name_plural = "学院"


class Program(models.Model):
    """专业方向表"""
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="programs", verbose_name="所属学院")
    program_id = models.CharField(max_length=10, verbose_name="专业ID", primary_key=True)
    program_name = models.CharField(max_length=100, verbose_name="专业名称")
    total_recruit = models.IntegerField(verbose_name="总招生人数")
    # 删除 recommended_recruit 字段
    remarks = models.TextField(blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return f"{self.program_name} ({self.program_id})"

    class Meta:
        verbose_name = "专业"
        verbose_name_plural = "专业"

class ResearchDirection(models.Model):
    """研究方向表"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="directions", verbose_name="所属专业")
    direction_id = models.CharField(max_length=10, verbose_name="研究方向ID")
    direction_name = models.CharField(max_length=100, verbose_name="研究方向名称")
    exam_subjects = models.TextField(verbose_name="考试科目")

    def __str__(self):
        return f"{self.direction_name} ({self.direction_id})"

    class Meta:
        verbose_name = "研究方向"
        verbose_name_plural = "研究方向"
        # 定义联合主键
        constraints = [
            models.UniqueConstraint(fields=['program', 'direction_id'], name='unique_program_direction')
        ]
class DirectionTeacher(models.Model):
    """研究方向与导师中间表"""
    direction = models.ForeignKey(ResearchDirection, on_delete=models.CASCADE, related_name="teachers", verbose_name="研究方向")
    teacher = models.ForeignKey(TeacherInfo, on_delete=models.CASCADE, related_name="directions", verbose_name="导师")

    def __str__(self):
        return f"{self.teacher} - {self.direction}"

    class Meta:
        verbose_name = "研究方向导师关联"
        verbose_name_plural = "研究方向导师关联"

class TeacherNameView(models.Model):
    TeacherID = models.CharField(max_length=10, primary_key=True, verbose_name='导师编号')
    Name = models.CharField(max_length=50, verbose_name='导师姓名')

    class Meta:
        managed = False  # 表示这是一个数据库视图，Django不会管理其迁移
        db_table = 'teachername'  # 数据库视图的名称


