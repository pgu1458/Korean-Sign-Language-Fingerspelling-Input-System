using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Drawing;
using System.Windows.Forms;
using Timer = System.Windows.Forms.Timer;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        private TcpListener server;
        private Thread listenThread;
        private bool isRunning = false;
        private string currentText = "";

        public Form1()
        {
            InitializeComponent();
            UpdateTime();
            Timer timer = new Timer();
            timer.Interval = 1000;
            timer.Tick += (s, e) => UpdateTime();
            timer.Start();
        }

        private void UpdateTime()
        {
            if (InvokeRequired)
                Invoke(new Action(() => lblTime.Text = DateTime.Now.ToString("HH:mm:ss")));
            else
                lblTime.Text = DateTime.Now.ToString("HH:mm:ss");
        }

        private void btnConnect_Click(object sender, EventArgs e)
        {
            if (isRunning) return;
            try
            {
                int port = (int)numPort.Value;
                server = new TcpListener(IPAddress.Any, port);
                server.Start();
                isRunning = true;

                listenThread = new Thread(ListenForClients);
                listenThread.IsBackground = true;
                listenThread.Start();

                SetStatus("대기중", Color.Yellow);
                AddLog("서버 시작 - 포트: " + port);
            }
            catch (Exception ex)
            {
                AddLog("오류: " + ex.Message);
            }
        }

        private void btnDisconnect_Click(object sender, EventArgs e)
        {
            isRunning = false;
            server?.Stop();
            SetStatus("연결 안됨", Color.Red);
            AddLog("서버 종료");
        }

        private void ListenForClients()
        {
            while (isRunning)
            {
                try
                {
                    TcpClient client = server.AcceptTcpClient();
                    AddLog("클라이언트 연결됨");
                    SetStatus("연결됨", Color.Lime);

                    Thread clientThread = new Thread(() => HandleClient(client));
                    clientThread.IsBackground = true;
                    clientThread.Start();
                }
                catch { break; }
            }
        }

        private void HandleClient(TcpClient client)
        {
            NetworkStream stream = client.GetStream();
            byte[] buffer = new byte[1024];
            string leftover = "";

            while (isRunning)
            {
                try
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead == 0) break;

                    string data = leftover + Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    string[] lines = data.Split('\n');

                    for (int i = 0; i < lines.Length - 1; i++)
                        ProcessPacket(lines[i].Trim());

                    leftover = lines[lines.Length - 1];
                }
                catch { break; }
            }

            AddLog("연결 끊김");
            SetStatus("연결 안됨", Color.Red);
            client.Close();
        }

        private void ProcessPacket(string packet)
        {
            if (string.IsNullOrEmpty(packet)) return;
            AddLog("수신: " + packet);

            if (packet.StartsWith("VOICE:"))
            {
                string ch = packet.Substring(6);
                AppendText(ch);
            }
            else if (packet.StartsWith("CHAR:"))
            {
                string ch = packet.Substring(5);
                AppendText(ch);
            }
            else if (packet == "CMD:DELETE")
            {
                DeleteLast();
            }
            else if (packet == "CMD:SPACE")
            {
                AppendText(" ");
            }
            else if (packet == "CMD:CLEAR")
            {
                ClearText();
            }
        }

        private void AppendText(string ch)
        {
            currentText += ch;
            UpdateDisplay();
        }

        private void DeleteLast()
        {
            if (currentText.Length > 0)
            {
                currentText = currentText.Substring(0, currentText.Length - 1);
                UpdateDisplay();
            }
        }

        private void ClearText()
        {
            currentText = "";
            UpdateDisplay();
        }

        private void UpdateDisplay()
        {
            if (InvokeRequired)
                Invoke(new Action(() => lblDisplay.Text = currentText));
            else
                lblDisplay.Text = currentText;
        }

        private void SetStatus(string status, Color color)
        {
            if (InvokeRequired)
                Invoke(new Action(() => {
                    lblStatus.Text = status;
                    lblStatus.ForeColor = color;
                }));
            else
            {
                lblStatus.Text = status;
                lblStatus.ForeColor = color;
            }
        }

        private void AddLog(string msg)
        {
            string log = $"[{DateTime.Now:HH:mm:ss}] {msg}";
            if (listLog.InvokeRequired)
                Invoke(new Action(() => {
                    listLog.Items.Add(log);
                    listLog.TopIndex = listLog.Items.Count - 1;
                }));
            else
            {
                listLog.Items.Add(log);
                listLog.TopIndex = listLog.Items.Count - 1;
            }
        }
    }
}