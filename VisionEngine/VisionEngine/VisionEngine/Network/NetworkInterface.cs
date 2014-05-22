using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;


namespace VisionEngine.Network
{
    class NetworkInterface
    {
        private NetworkBuffer _Buffer;
        private TcpClient  clientSocket = new TcpClient();
        private NetworkStream serverStream;

        public NetworkInterface(NetworkBuffer _Buffer)
        {
            this._Buffer = _Buffer;
            this.clientSocket.Connect("192.168.178.26", 1337);
            this.serverStream = clientSocket.GetStream();
        }

        public void Send(string Data)
        {
            byte[] outStream = System.Text.Encoding.ASCII.GetBytes(Data);
            this.serverStream.Write(outStream, 0, outStream.Length);
           // this.serverStream.Flush();

        }

        public void Recv()
        {
            byte[] inStream = new byte[1024];
            
            string Data = string.Empty;
            
            while (!Data.Contains("<EOF>"))
            {
                serverStream.Read(inStream, 0, 1024);
                Data += Encoding.ASCII.GetString(inStream);
            }

            _Buffer.Append(Data.Substring(0, Data.Length - 5));
        }

        public void Disconnect()
        {
            serverStream.Dispose();
        }

    }
}
