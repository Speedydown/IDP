using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VisionEngine
{
    class Balloon :IComparable<Balloon>
    {
        public int index { get; private set;}
        public Color color { get; private set; }
        private string script = "findballoon";

        public Balloon(int index, Color color) {
            this.index = index;
            this.color = color;
            switch (color.Name) {
                case "Red":
                    script = "findBalloonRed";
                    break;
                case "Green":
                    script = "findBalloonGreen";
                    break;
                case "Blue":
                    script = "findBalloonBlue";
                    break;                    
            }

            Console.WriteLine(color.Name);
        }

        public void findBalloon()
        {
            JL_VisionLib_V3.CmdInt.Execute("addScript findballoon findBalloon" + this.color.Name +".jls");
            JL_VisionLib_V3.CmdInt.Execute("icall findballoon");
        }

        public int CompareTo(Balloon b2)
        {
            return this.index.CompareTo(b2.index);
        }
    }

}
