namespace WinFormsApp1
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            lblStatus = new Label();
            lblDisplay = new Label();
            lblTime = new Label();
            lblReady = new Label();
            lblDetecting = new Label();
            lblHold = new Label();
            lblConfirmed = new Label();
            lblError = new Label();
            numPort = new NumericUpDown();
            numHoldTime = new NumericUpDown();
            numCamera = new NumericUpDown();
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            btnConnect = new Button();
            btnDisconnect = new Button();
            listLog = new ListBox();
            ((System.ComponentModel.ISupportInitialize)numPort).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numHoldTime).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numCamera).BeginInit();
            SuspendLayout();
            // 
            // lblStatus
            // 
            lblStatus.AutoSize = true;
            lblStatus.Location = new Point(437, 9);
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(69, 20);
            lblStatus.TabIndex = 0;
            lblStatus.Text = "연결상태";
            // 
            // lblDisplay
            // 
            lblDisplay.AutoSize = true;
            lblDisplay.Location = new Point(206, 89);
            lblDisplay.Name = "lblDisplay";
            lblDisplay.Size = new Size(89, 20);
            lblDisplay.TabIndex = 1;
            lblDisplay.Text = "결과 표시창";
            // 
            // lblTime
            // 
            lblTime.AutoSize = true;
            lblTime.Location = new Point(759, 9);
            lblTime.Name = "lblTime";
            lblTime.Size = new Size(39, 20);
            lblTime.TabIndex = 2;
            lblTime.Text = "시간";
            // 
            // lblReady
            // 
            lblReady.AutoSize = true;
            lblReady.Location = new Point(26, 21);
            lblReady.Name = "lblReady";
            lblReady.Size = new Size(50, 20);
            lblReady.TabIndex = 3;
            lblReady.Text = "Ready";
            // 
            // lblDetecting
            // 
            lblDetecting.AutoSize = true;
            lblDetecting.Location = new Point(26, 132);
            lblDetecting.Name = "lblDetecting";
            lblDetecting.Size = new Size(75, 20);
            lblDetecting.TabIndex = 4;
            lblDetecting.Text = "Detecting";
            // 
            // lblHold
            // 
            lblHold.AutoSize = true;
            lblHold.Location = new Point(26, 239);
            lblHold.Name = "lblHold";
            lblHold.Size = new Size(42, 20);
            lblHold.TabIndex = 5;
            lblHold.Text = "Hold";
            // 
            // lblConfirmed
            // 
            lblConfirmed.AutoSize = true;
            lblConfirmed.Location = new Point(26, 324);
            lblConfirmed.Name = "lblConfirmed";
            lblConfirmed.Size = new Size(81, 20);
            lblConfirmed.TabIndex = 6;
            lblConfirmed.Text = "Confirmed";
            // 
            // lblError
            // 
            lblError.AutoSize = true;
            lblError.Location = new Point(26, 418);
            lblError.Name = "lblError";
            lblError.Size = new Size(41, 20);
            lblError.TabIndex = 7;
            lblError.Text = "Error";
            // 
            // numPort
            // 
            numPort.Location = new Point(1044, 168);
            numPort.Maximum = new decimal(new int[] { 65535, 0, 0, 0 });
            numPort.Name = "numPort";
            numPort.Size = new Size(160, 27);
            numPort.TabIndex = 8;
            // 
            // numHoldTime
            // 
            numHoldTime.Location = new Point(1044, 253);
            numHoldTime.Name = "numHoldTime";
            numHoldTime.Size = new Size(160, 27);
            numHoldTime.TabIndex = 9;
            // 
            // numCamera
            // 
            numCamera.Location = new Point(1044, 347);
            numCamera.Name = "numCamera";
            numCamera.Size = new Size(160, 27);
            numCamera.TabIndex = 10;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(1044, 145);
            label1.Name = "label1";
            label1.Size = new Size(39, 20);
            label1.TabIndex = 11;
            label1.Text = "포트";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(1044, 230);
            label2.Name = "label2";
            label2.Size = new Size(75, 20);
            label2.TabIndex = 12;
            label2.Text = "HoldTime";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(1044, 320);
            label3.Name = "label3";
            label3.Size = new Size(103, 20);
            label3.TabIndex = 13;
            label3.Text = "Camera Index";
            // 
            // btnConnect
            // 
            btnConnect.Location = new Point(1001, 437);
            btnConnect.Name = "btnConnect";
            btnConnect.Size = new Size(94, 29);
            btnConnect.TabIndex = 14;
            btnConnect.Text = "연결";
            btnConnect.UseVisualStyleBackColor = true;
            btnConnect.Click += btnConnect_Click;
            // 
            // btnDisconnect
            // 
            btnDisconnect.Location = new Point(1110, 437);
            btnDisconnect.Name = "btnDisconnect";
            btnDisconnect.Size = new Size(94, 29);
            btnDisconnect.TabIndex = 15;
            btnDisconnect.Text = "연결종료";
            btnDisconnect.UseVisualStyleBackColor = true;
            btnDisconnect.Click += btnDisconnect_Click;
            // 
            // listLog
            // 
            listLog.FormattingEnabled = true;
            listLog.Location = new Point(26, 472);
            listLog.Name = "listLog";
            listLog.Size = new Size(1178, 124);
            listLog.TabIndex = 16;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1231, 614);
            Controls.Add(listLog);
            Controls.Add(btnDisconnect);
            Controls.Add(btnConnect);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(numCamera);
            Controls.Add(numHoldTime);
            Controls.Add(numPort);
            Controls.Add(lblError);
            Controls.Add(lblConfirmed);
            Controls.Add(lblHold);
            Controls.Add(lblDetecting);
            Controls.Add(lblReady);
            Controls.Add(lblTime);
            Controls.Add(lblDisplay);
            Controls.Add(lblStatus);
            Name = "Form1";
            Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)numPort).EndInit();
            ((System.ComponentModel.ISupportInitialize)numHoldTime).EndInit();
            ((System.ComponentModel.ISupportInitialize)numCamera).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label lblStatus;
        private Label lblDisplay;
        private Label lblTime;
        private Label lblReady;
        private Label lblDetecting;
        private Label lblHold;
        private Label lblConfirmed;
        private Label lblError;
        private NumericUpDown numPort;
        private NumericUpDown numHoldTime;
        private NumericUpDown numCamera;
        private Label label1;
        private Label label2;
        private Label label3;
        private Button btnConnect;
        private Button btnDisconnect;
        private ListBox listLog;
    }
}
