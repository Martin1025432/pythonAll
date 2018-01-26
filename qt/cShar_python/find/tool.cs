using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Cognex.VisionPro.Caliper;
using Cognex.VisionPro;
using Cognex.VisionPro.ImageFile;
using Cognex.VisionPro.PixelMap;
using Cognex.VisionPro.ToolGroup;
using Cognex.VisionPro.Blob;
using Cognex.VisionPro.QuickBuild;


namespace find
{
    public class tool
    {
        public static List<double> find(int toolNum,int method)
        {
            object toolgroup = CogSerializer.LoadObjectFromFile("c://tool.vpp");
            object job = CogSerializer.LoadObjectFromFile("QuickBuild1.vpp");
            
            switch (toolNum)
            {
                case 0:  toolgroup = CogSerializer.LoadObjectFromFile("c://tool0.vpp");
                    break;
                case 1:  toolgroup = CogSerializer.LoadObjectFromFile("c://tool1.vpp");
                    break;
                case 2: toolgroup = CogSerializer.LoadObjectFromFile("c://tool2.vpp");
                    break;
                case 3: toolgroup = CogSerializer.LoadObjectFromFile("c://tool3.vpp");
                    break;
                default: break;

            } 
            
            CogToolGroup ToolGroup1 = toolgroup as CogToolGroup;
            CogJobManager cojob = job as CogJobManager;
            CogJob cojob = cojob.Job["CogJob1"] as CogJob;
           
            
            CogImageFileTool myFile = ToolGroup1.Tools["CogImageFileTool1"] as CogImageFileTool;
            myFile.Run();
            CogFindCircleTool myCircleTool = ToolGroup1.Tools["CogFindCircleTool1"] as CogFindCircleTool;
            CogFindLineTool myLineTool = ToolGroup1.Tools["CogFindLineTool1"] as CogFindLineTool;
            switch (method)
            {
                case 1: myCircleTool.Run();
                    break;
                case 2: myLineTool.Run();
                    break;
                case 3: myCircleTool.Run();
                        myLineTool.Run();
                        break;               
                default: break;
            }
            double Lx0=0;
            double Lx1=0;
            double Ly0=0;
            double Ly1=0;
            double Langle=0;
            double Cx=0;
            double Cy=0;
            double Cr=0;
            

            if (method == 1 | method == 3)
                {
                    Cx = myCircleTool.Results.GetCircle().CenterX;
                    Cy = myCircleTool.Results.GetCircle().CenterY;
                    Cr = myCircleTool.Results.GetCircle().Radius;
                }
             if (method == 2 | method == 3)
                {
                     Lx0 = myLineTool.Results.GetLineSegment().StartX;
                     Ly0 = myLineTool.Results.GetLineSegment().StartY;
                     Lx1 = myLineTool.Results.GetLineSegment().EndX;
                     Ly1 = myLineTool.Results.GetLineSegment().EndY;
                     Langle = myLineTool.Results.GetLine().Rotation;
                }
            double[] result = { Cx, Cy, Cr, Lx0, Ly0, Lx1, Ly1, Langle };
            return new List<double>(result);
        }

   
    }
}
