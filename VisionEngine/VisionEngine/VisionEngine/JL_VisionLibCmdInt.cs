/* File     : JL_VisionLibCmdInt.cs 
 * Project  : visionlib V3.0
 * Author   : Dick Bruin and Jaap van de Loosdrecht
 *            Van de Loosdrecht Machine Vision BV
 *            www.vdlmv.nl
 * Date     : 20-12-2009
 *
 * Copyright (c) 1993-2009, Van de Loosdrecht Machine Vision,
 * all rights reserved.
 * 
 * This module is a wrapper around JL_VisionLib_DLL.dll.
 * This is now the preferred way to interface VisionLab with .Net. 
 * The old way by using JL_VisionLib_Net.dll is now deprecated.
 * 
 * NOTE:
 * - the string dllName will specify the place of JL_VisionLib_DLL.dll.
 */


using System;
using System.Drawing;
using System.Text;
using System.Runtime.InteropServices;

namespace JL_VisionLib_V3

{
	/// <summary>
	/// Summary description for VisionLib.
	/// interface to JL_VisionLib_DLL.dll
	/// Init		- call this as soon as possible to avoid late loading (and license file problems)
	/// Execute		- excute a visionlab command
	/// GetImage	- downloads a bitmap image
	/// SetImage	- uploads a bitmap image
	/// </summary>
	public class CmdInt
	{
        // protected const string dllName = @"..\..\..\release\JL_VisionLib_DLL.dll";
        protected const string dllName = @"..\..\..\Vision\JL_VisionLib_DLL.dll";
        
        [DllImport(dllName, CallingConvention = CallingConvention.Cdecl)]
        protected static extern int JL_Execute(string cmd, StringBuilder answer, int maxSizeAnswer);

        [DllImport(dllName, CallingConvention = CallingConvention.Cdecl)]
        protected static extern IntPtr JL_GetImage(string imageName, StringBuilder answer, int maxSizeAnswer);

        [DllImport(dllName, CallingConvention = CallingConvention.Cdecl)]
        protected static extern int JL_SetImage(string imageName, string imagetype, IntPtr bmpH, StringBuilder answer, int maxSizeAnswer);

        [DllImport("gdi32.dll")]
        protected static extern bool DeleteObject(IntPtr hObject);

        private static StringBuilder msgBuffer = new StringBuilder(100000);  // size a largest string result expected

        private static string StripAnswer(StringBuilder answer)
        {
            string msg = msgBuffer.ToString();
            int p = msg.LastIndexOf('{');
            if (p != -1) msg = msg.Substring(0, p); // remove {time us} msg
            if ((msg.Length > 0) && (msg[msg.Length - 1] == '\n'))
                msg = msg.Substring(0, msg.Length - 1);  // remove last \n
            if ((msg.Length > 0) && (msg[0] == '['))
                throw new System.ApplicationException(msg);
            return msg;
        }

		public static string Init()
		{
			return Execute("version");
		}

		public static string Execute(string cmd)
		{
            JL_Execute(cmd, msgBuffer, msgBuffer.Capacity);
            return StripAnswer(msgBuffer);
		}

		public static Bitmap GetImage(string imageName)
		{
            IntPtr h = JL_GetImage(imageName, msgBuffer, msgBuffer.Capacity);
            if (h == (IntPtr)0)
                throw new System.ApplicationException(msgBuffer.ToString());
            Bitmap bm = System.Drawing.Image.FromHbitmap(h);
            DeleteObject(h);
            return bm;
		}

		public static void SetImage(string imageName, string imageType, Bitmap bmp)
		{
            IntPtr h = bmp.GetHbitmap();
            JL_SetImage(imageName, imageType, h, msgBuffer, msgBuffer.Capacity);
            DeleteObject(h);
            StripAnswer(msgBuffer);
		}

	}
}
