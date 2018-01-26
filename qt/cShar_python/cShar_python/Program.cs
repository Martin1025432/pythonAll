using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace cShar_python
{
    class Program
    {
        static void Main(string[] args)
        {
          //   Console.WriteLine("请输入要执行的命令:");
          //   string strInput = Console.ReadLine();
             Process p = new Process();
             //设置要启动的应用程序
             p.StartInfo.FileName = "cmd.exe";
            //是否使用操作系统shell启动
             p.StartInfo.UseShellExecute = false;
             // 接受来自调用程序的输入信息
             p.StartInfo.RedirectStandardInput = false;
             //输出信息
             p.StartInfo.RedirectStandardOutput = false;
             // 输出错误
             p.StartInfo.RedirectStandardError = true;
             //不显示程序窗口
             p.StartInfo.CreateNoWindow = true;
             //启动程序
             p.StartInfo.Arguments = "/C " + "python pyqt_first.py";
             p.Start();
 
             //向cmd窗口发送输入信息
           //  p.StandardInput.WriteLine("python pyqt_first.py"+"&exit");
 
         //    p.StandardInput.AutoFlush=true;
 
              //获取输出信息
           //  string strOuput = p.StandardOutput.ReadToEnd();
             //等待程序执行完退出进程
          //   p.WaitForExit();
     //        p.Close();
       //      Console.WriteLine(strOuput);
      //       Console.ReadKey();

        }

        private static void doPython(string StartFileName, string StartFileArg)
        {
            Process CmdProcess = new Process();
            CmdProcess.StartInfo.FileName = StartFileName;      // 命令  
            CmdProcess.StartInfo.Arguments = StartFileArg;      // 参数  

            CmdProcess.StartInfo.CreateNoWindow = true;         // 不创建新窗口  
            CmdProcess.StartInfo.UseShellExecute = false;
            CmdProcess.StartInfo.RedirectStandardInput = true;  // 重定向输入  
            CmdProcess.StartInfo.RedirectStandardOutput = true; // 重定向标准输出  
            CmdProcess.StartInfo.RedirectStandardError = true;  // 重定向错误输出  
            //CmdProcess.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;  



            CmdProcess.Start();


        }
    }
}
