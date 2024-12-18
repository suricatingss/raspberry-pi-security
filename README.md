<h2>The Home Security solution for Raspberry Pi!</h2>
<br>
<p>This is a student-made project that shows the potential of normal components and mount them into a custom-made home security</p>
<p>The components used are not expensive at all (except for the Raspberry Pi, which might cost you a bit). Sensors like PIR and REED are unexpensive and perfect for this type of project.<br>
You can even use that old webcam of yours for a security camera :)</p>

<h4>Components</h4>
<p>What you need for this project is:</p>
<ul>
  <li>Raspberry Pi (Recommended 3 and above. Dont run it on a Pi Pico)</li>
  <li>Some reed sensors (for doors and windows)</li>
  <li>Some PIR sensors (for movements)</li>
  <li>Some USB webcams (optional)</li>
  <li>A 3x4 numpad <b>or</b><br>A TFT screen for the GUI.<br>(You can continue without either, but you will be entirely dependent of the Web GUI.)</li>
  <li><s>Some hot chocolate pie</s></li>
</ul>

<h4>How it works</h4>
<p>This project was made on <b>Python</b>, mostly. <br>There are many python modules for many things, such as cameras, sensor detection, users logging.</p>
<p>You can arm and disarm the system by directly interacting with it (TFT screen or 3x4 keypad) or via WebGUI.</p>
<p>Yes, this project counts with a Web GUI controller that allows you to manage remotely the system directly from your phone's browser. Everything is done on the Web, since state changes, user management, other settings, consulting cameras, etc.</p>
<p>But the keypad is there for a faster interaction when you need it, so you still have a way of disarming it even if your phone dies ;)</p>

<h4>Features</h4>
<ul>
  <li>User authentication</li>
  <li>Detailed logs (MySQL)</li>
  <li>Web GUI management</li>
  <li>Ease of interaction</li>
  <li>Customization</li>
</ul>

<h4>Languages used</h4>
<p><b>Python</b>, like said early, was the main language used for the program. It was used to:<br>
  <ul>
    <li>Communicate with the hardware</li>
    <li>Process manual commands</li>
    <li>Background processing</li>
    <li>Database communication</li>
    <li>Data streaming</li>
  </ul>
  
<p>For the <b>Web GUI</b>:<br>
  <ul>
  <li>HTML and CSS, as you guessed, to properly display the page.</li>
  <li>JS was used for diverse tasks, such as background checks, displaying relevant content and handle input data.</li>
  <li>PHP was the most used. Besides serving as a safe authentication and providing a safe way to submit data to the server, 
  it also changes the WebGUI to reflect more sensitive data without exposing anything.<br>
  Its use was <b>crucial</b> in making the Web GUI well-protected. It was the most used one out of all 4.</li>
  </ul>
</p>
  
<h4>Downloads</h4>
<p>Here on GitHub is the Python Project made on Windows and uploaded via <b>PyCharm</b> (for exploring the code only, not installation)<br>
To install the project, I got the zipped components ready to download via the links below.<br>
You can either <b>install the components yourself</b> or <b>run the installer</b>. It's up to you</p>
[Show Files](target="https://suricatingss.xyz/nextcloud/index.php/s/ARrYTe69qzrbqwd)
[Download Python Project (without venv)](https://suricatingss.xyz/nextcloud/index.php/s/ARrYTe69qzrbqwd/download?path=%2F&files=python_prog.zip)
[Download Web GUI files](https://suricatingss.xyz/nextcloud/index.php/s/ARrYTe69qzrbqwd/download?path=%2F&files=safe-gui.zip)
