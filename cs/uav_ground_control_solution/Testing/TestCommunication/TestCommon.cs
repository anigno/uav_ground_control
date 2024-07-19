using communication.http2;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Testing.TestCommunication
{

    internal class TestCommon
    {
        private Http2Communicator comm = new Http2Communicator("127.0.0.1", 1001);

        public TestCommon()
        {
            comm.Start();
        }
        public static void Main()
        {
            new TestCommon();
            Console.WriteLine("enter to exit");
            Console.ReadLine();
        }
    }
}
