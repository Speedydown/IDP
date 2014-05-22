using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace VisionEngine.Network
{
    class NetworkBuffer
    {
        private Stack<string> Buffer;
        private Semaphore BufferSemaphore;


        public NetworkBuffer()
        {
            Buffer = new Stack<string>();
            BufferSemaphore = new Semaphore(1, 1);
        }


        public void Append(string Data)
        {
            BufferSemaphore.WaitOne();
            Buffer.Push(Data);
            BufferSemaphore.Release();
        }


        public string Get()
        {
            BufferSemaphore.WaitOne();
            string Data = Buffer.Pop();
            BufferSemaphore.Release();
            return Data;
        }
    }

}
