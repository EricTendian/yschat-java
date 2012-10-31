import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import javax.swing.*;
import javax.swing.table.*;
import javax.swing.text.Document;

public class YSC_applet extends JApplet {
    private YSChat yschat = new YSChat();
    public static DefaultTableModel model = new javax.swing.table.DefaultTableModel(new Object [][] {}, new String [] {"ID", "Username", "IFF"});
    public static File log;
    public static BufferedWriter log_out;
    public static URL logfileURL;
    
    /** Creates new form YSC_gui */
    public YSC_applet() {
        initComponents();
        try {
            URL url = new URL("http://www.yspilots.com/shadowhunters/rssList.php");
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            String s;
            while ((s = in.readLine()) != null) {
                if (s.indexOf("http://www.yspilots.com/shadowhunters/get_info.php?ip=")!=-1) 
                    ipBox.addItem(s.substring(s.indexOf("http://www.yspilots.com/shadowhunters/get_info.php?ip=")+54, s.indexOf("&amp;port=")));
            }
            in.close();
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Impossible to get the online server list!", "YS_chat", JOptionPane.ERROR_MESSAGE);
        }
        
        try {
            logfileURL = new URL("file:/"+System.getProperty("user.dir")+"/logfile"+ new SimpleDateFormat("yyyyMMdd").format(new Date())+".htm");
            log = new File(logfileURL.toURI());
            
            if (!log.exists()) {log_out = new BufferedWriter(new FileWriter(log)); log_out.append("<HEAD><LINK REL=STYLESHEET HREF=\"ysc_colors.css\" TYPE=\"text/css\"></HEAD>"); log_out.flush();}
            else log_out = new BufferedWriter(new FileWriter(log, true));
            refresh();
        } catch (Exception ex) {
            System.out.println("cannot create logfile!");
            ex.printStackTrace();
        }
    }

    public static void refresh() throws IOException {
        log_out.flush();
        Document doc = messOut.getDocument();
        doc.putProperty(Document.StreamDescriptionProperty, null);
        messOut.setPage(logfileURL);
        messOut.setEditable(true);messOut.setCaretPosition(messOut.getDocument().getLength());messOut.setEditable(false);
    }
    private void connect() {
        ipBox.setSelectedItem(ipBox.getSelectedItem().toString().trim());
        yschat.setIp(ipBox.getSelectedItem().toString());
        yschat.setPort(portBox.getText());
        yschat.setUsername(userBox.getText());
        try {
            int vers = Integer.parseInt(versionBox.getText().substring(0,8));
            String version = "0"+Integer.toHexString(vers);
            version=version.substring(6)+version.substring(4,6)+version.substring(2,4)+version.substring(0,2);
            yschat.setVersion(version);
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "You must put a number in the version box!", "YS_chat", JOptionPane.ERROR_MESSAGE);
        }
        try {
            yschat.connect();
            connectButton.setEnabled(false);
            connectItem.setEnabled(false);
            disconnButton.setEnabled(true);
            disconnItem.setEnabled(true);
            messIn.setEnabled(true);
            messIn.setEditable(true);
            playerList.setEnabled(true);
            yschat.listPlayers();
            yschat.servInfo();
            versionBox.setText(yschat.version);
            mapBox.setText(yschat.map);
            log_out.append("<p>"+yschat.format("Connection on "+yschat.getIp()+":"+yschat.getPort()+" on "+new SimpleDateFormat("E, dd MMM yyyy [HH:mm:ss]").format(new Date())+" with the username "+yschat.getUsername(), "ys_chat_mess")+"<br/>");
            refresh();
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "ERROR CONNECTING TO SERVER\n"+ex, "YS_chat", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void disconnect() {
        try {
            yschat.disconnect();
            log_out.append(yschat.format("Connection stopped at "+new SimpleDateFormat("[HH:mm:ss]").format(new Date()), "ys_chat_mess")+"</p>");
            refresh();
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "ERROR DISCONNECTING FROM SERVER\n"+ex, "YS_chat", JOptionPane.ERROR_MESSAGE);
        }
        mapBox.setText("");
        connectButton.setEnabled(true);
        connectItem.setEnabled(true);
        disconnButton.setEnabled(false);
        disconnItem.setEnabled(false);
        messIn.setEnabled(false);
        messIn.setEditable(false);
        playerList.setEnabled(false);
        model.setRowCount(0);
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        about = new javax.swing.JDialog();
        jOptionPane1 = new javax.swing.JOptionPane();
        YSCgui = new javax.swing.JInternalFrame();
        topPanel = new javax.swing.JPanel();
        versionBox = new javax.swing.JTextField();
        userBox = new javax.swing.JTextField();
        ipBox = new javax.swing.JComboBox();
        portBox = new javax.swing.JTextField();
        connectButton = new javax.swing.JButton();
        servernameBox = new javax.swing.JTextField();
        mapLabel = new javax.swing.JLabel();
        disconnButton = new javax.swing.JButton();
        mapBox = new javax.swing.JTextField();
        servInfo = new javax.swing.JButton();
        splitPane = new javax.swing.JSplitPane();
        leftPane = new javax.swing.JPanel();
        playersLabel = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        playerList = new javax.swing.JTable();
        automess = new javax.swing.JCheckBox();
        autoserver = new javax.swing.JCheckBox();
        automap = new javax.swing.JCheckBox();
        rightPane = new javax.swing.JPanel();
        messScroll = new javax.swing.JScrollPane();
        messOut = new javax.swing.JEditorPane();
        messIn = new javax.swing.JTextField();
        menu = new javax.swing.JMenuBar();
        fileMenu = new javax.swing.JMenu();
        connectItem = new javax.swing.JMenuItem();
        disconnItem = new javax.swing.JMenuItem();
        servList = new javax.swing.JMenuItem();
        jSeparator1 = new javax.swing.JPopupMenu.Separator();
        exitItem = new javax.swing.JMenuItem();
        insertMenu = new javax.swing.JMenu();
        jMenu1 = new javax.swing.JMenu();
        jMenuItem2 = new javax.swing.JMenuItem();
        jMenuItem3 = new javax.swing.JMenuItem();
        jMenuItem4 = new javax.swing.JMenuItem();
        jMenuItem5 = new javax.swing.JMenuItem();
        jMenuItem6 = new javax.swing.JMenuItem();
        jMenuItem7 = new javax.swing.JMenuItem();
        jMenuItem8 = new javax.swing.JMenuItem();
        jMenuItem9 = new javax.swing.JMenuItem();
        jMenu2 = new javax.swing.JMenu();
        jMenuItem11 = new javax.swing.JMenuItem();
        jMenuItem12 = new javax.swing.JMenuItem();
        jMenuItem13 = new javax.swing.JMenuItem();
        jMenuItem14 = new javax.swing.JMenuItem();
        jMenuItem15 = new javax.swing.JMenuItem();
        jMenuItem16 = new javax.swing.JMenuItem();
        jMenuItem17 = new javax.swing.JMenuItem();
        jMenuItem18 = new javax.swing.JMenuItem();
        jMenuItem19 = new javax.swing.JMenuItem();
        jMenuItem20 = new javax.swing.JMenuItem();
        jMenuItem21 = new javax.swing.JMenuItem();
        jMenuItem22 = new javax.swing.JMenuItem();
        jMenuItem23 = new javax.swing.JMenuItem();
        jMenuItem24 = new javax.swing.JMenuItem();
        yspsMenu = new javax.swing.JMenu();
        jMenu3 = new javax.swing.JMenu();
        jMenuItem26 = new javax.swing.JMenuItem();
        jMenuItem27 = new javax.swing.JMenuItem();
        jMenuItem28 = new javax.swing.JMenuItem();
        jMenuItem29 = new javax.swing.JMenuItem();
        jMenuItem30 = new javax.swing.JMenuItem();
        jMenuItem31 = new javax.swing.JMenuItem();
        jMenuItem32 = new javax.swing.JMenuItem();
        jMenuItem33 = new javax.swing.JMenuItem();
        jMenuItem34 = new javax.swing.JMenuItem();
        jMenuItem35 = new javax.swing.JMenuItem();
        jMenuItem36 = new javax.swing.JMenuItem();
        jMenuItem37 = new javax.swing.JMenuItem();
        jMenuItem38 = new javax.swing.JMenuItem();
        jMenuItem39 = new javax.swing.JMenuItem();
        jMenuItem40 = new javax.swing.JMenuItem();
        jMenuItem41 = new javax.swing.JMenuItem();
        jMenuItem42 = new javax.swing.JMenuItem();
        jMenu4 = new javax.swing.JMenu();
        jMenuItem44 = new javax.swing.JMenuItem();
        jMenuItem45 = new javax.swing.JMenuItem();
        jMenuItem46 = new javax.swing.JMenuItem();
        jMenuItem47 = new javax.swing.JMenuItem();
        jMenuItem48 = new javax.swing.JMenuItem();
        jMenuItem49 = new javax.swing.JMenuItem();
        jMenuItem50 = new javax.swing.JMenuItem();
        jMenuItem51 = new javax.swing.JMenuItem();
        jMenuItem52 = new javax.swing.JMenuItem();
        jMenuItem53 = new javax.swing.JMenuItem();
        helpMenu = new javax.swing.JMenu();
        aboutItem = new javax.swing.JMenuItem();
        helpItem = new javax.swing.JMenuItem();

        about.setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);
        about.setTitle("About YSChat");

        jOptionPane1.setMessage("YSChat [Java ed.] version 0.5 by erict15\nOriginal Python program by VincentWeb");
        jOptionPane1.setMessageType(1);

        javax.swing.GroupLayout aboutLayout = new javax.swing.GroupLayout(about.getContentPane());
        about.getContentPane().setLayout(aboutLayout);
        aboutLayout.setHorizontalGroup(
            aboutLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jOptionPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 320, javax.swing.GroupLayout.PREFERRED_SIZE)
        );
        aboutLayout.setVerticalGroup(
            aboutLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jOptionPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 110, javax.swing.GroupLayout.PREFERRED_SIZE)
        );

        YSCgui.setBorder(null);
        YSCgui.setTitle("YSC: YS Chat");
        YSCgui.setOpaque(true);
        YSCgui.setPreferredSize(new java.awt.Dimension(782, 580));
        try {
            YSCgui.setSelected(true);
        } catch (java.beans.PropertyVetoException e1) {
            e1.printStackTrace();
        }
        YSCgui.setVisible(true);

        versionBox.setForeground(new java.awt.Color(255, 0, 0));
        versionBox.setText("20080220");
        versionBox.setToolTipText("YS server version");

        userBox.setForeground(new java.awt.Color(0, 0, 255));
        userBox.setText("your username here");
        userBox.setToolTipText("username");

        ipBox.setEditable(true);
        ipBox.setToolTipText("Server IP");

        portBox.setBackground(new java.awt.Color(238, 238, 238));
        portBox.setForeground(new java.awt.Color(136, 136, 0));
        portBox.setText("7915");
        portBox.setToolTipText("Server Port");

        connectButton.setText("Connect");
        connectButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                connectButtonActionPerformed(evt);
            }
        });

        servernameBox.setBackground(new java.awt.Color(187, 187, 255));
        servernameBox.setToolTipText("server name");

        mapLabel.setText("Map:");

        disconnButton.setText("Disconnect");
        disconnButton.setEnabled(false);
        disconnButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disconnButtonActionPerformed(evt);
            }
        });

        mapBox.setEditable(false);

        servInfo.setText("Server Info");
        servInfo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                servInfoActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout topPanelLayout = new javax.swing.GroupLayout(topPanel);
        topPanel.setLayout(topPanelLayout);
        topPanelLayout.setHorizontalGroup(
            topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(topPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(versionBox, javax.swing.GroupLayout.PREFERRED_SIZE, 71, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(servernameBox, javax.swing.GroupLayout.PREFERRED_SIZE, 145, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(37, 37, 37)
                .addGroup(topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(topPanelLayout.createSequentialGroup()
                        .addComponent(userBox, javax.swing.GroupLayout.PREFERRED_SIZE, 132, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ipBox, javax.swing.GroupLayout.PREFERRED_SIZE, 147, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(portBox, javax.swing.GroupLayout.PREFERRED_SIZE, 37, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(42, 42, 42)
                        .addComponent(connectButton)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(disconnButton))
                    .addGroup(topPanelLayout.createSequentialGroup()
                        .addComponent(mapLabel)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(mapBox, javax.swing.GroupLayout.PREFERRED_SIZE, 139, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(servInfo)))
                .addContainerGap(46, Short.MAX_VALUE))
        );
        topPanelLayout.setVerticalGroup(
            topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(topPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(topPanelLayout.createSequentialGroup()
                        .addGap(6, 6, 6)
                        .addComponent(versionBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(servernameBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(topPanelLayout.createSequentialGroup()
                        .addGroup(topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(userBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(ipBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(portBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(connectButton)
                            .addComponent(disconnButton))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(topPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(mapLabel)
                            .addComponent(mapBox, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(servInfo))))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        splitPane.setDividerLocation(160);
        splitPane.setAutoscrolls(true);
        splitPane.setOneTouchExpandable(true);
        splitPane.setPreferredSize(new java.awt.Dimension(850, 479));

        leftPane.setAutoscrolls(true);

        playersLabel.setText("Players:");

        playerList.setFont(new java.awt.Font("Tahoma", 0, 10));
        playerList.setModel(model);
        playerList.setAutoResizeMode(javax.swing.JTable.AUTO_RESIZE_ALL_COLUMNS);
        playerList.setEnabled(false);
        playerList.getTableHeader().setReorderingAllowed(false);
        jScrollPane1.setViewportView(playerList);

        automess.setText("automess");

        autoserver.setText("autoserver");

        automap.setText("automap");

        javax.swing.GroupLayout leftPaneLayout = new javax.swing.GroupLayout(leftPane);
        leftPane.setLayout(leftPaneLayout);
        leftPaneLayout.setHorizontalGroup(
            leftPaneLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(leftPaneLayout.createSequentialGroup()
                .addGroup(leftPaneLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(playersLabel)
                    .addGroup(leftPaneLayout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(autoserver))
                    .addGroup(leftPaneLayout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(automess))
                    .addGroup(leftPaneLayout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(automap)))
                .addContainerGap(74, Short.MAX_VALUE))
            .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 159, Short.MAX_VALUE)
        );
        leftPaneLayout.setVerticalGroup(
            leftPaneLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(leftPaneLayout.createSequentialGroup()
                .addComponent(playersLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 361, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(automess)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(autoserver)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(automap)
                .addContainerGap())
        );

        splitPane.setLeftComponent(leftPane);

        messOut.setContentType("text/html");
        messOut.setEditable(false);
        messOut.addPropertyChangeListener(new PropertyChangeListener() {
            public void propertyChange(PropertyChangeEvent e) {
                if (e.getPropertyName().equals("page")) {
                    messScroll.getVerticalScrollBar().setValue(messScroll.getVerticalScrollBar().getMaximum());
                }
            }
        });
        messScroll.setViewportView(messOut);

        messIn.setEditable(false);
        messIn.setEnabled(false);
        messIn.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent evt) {
                messInKeyReleased(evt);
            }
        });

        javax.swing.GroupLayout rightPaneLayout = new javax.swing.GroupLayout(rightPane);
        rightPane.setLayout(rightPaneLayout);
        rightPaneLayout.setHorizontalGroup(
            rightPaneLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(messScroll, javax.swing.GroupLayout.DEFAULT_SIZE, 616, Short.MAX_VALUE)
            .addComponent(messIn, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, 616, Short.MAX_VALUE)
        );
        rightPaneLayout.setVerticalGroup(
            rightPaneLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, rightPaneLayout.createSequentialGroup()
                .addComponent(messScroll, javax.swing.GroupLayout.DEFAULT_SIZE, 433, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(messIn, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
        );

        splitPane.setRightComponent(rightPane);

        fileMenu.setText("File");

        connectItem.setText("Connect");
        connectItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                connectItemconnectButtonActionPerformed(evt);
            }
        });
        fileMenu.add(connectItem);

        disconnItem.setText("Disconnect");
        disconnItem.setEnabled(false);
        disconnItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                disconnItemdisconnButtonActionPerformed(evt);
            }
        });
        fileMenu.add(disconnItem);

        servList.setText("Online Server List");
        servList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                servListActionPerformed(evt);
            }
        });
        fileMenu.add(servList);
        fileMenu.add(jSeparator1);

        exitItem.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_F4, java.awt.event.InputEvent.ALT_MASK));
        exitItem.setText("Exit");
        exitItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                exitItemActionPerformed(evt);
            }
        });
        fileMenu.add(exitItem);

        menu.add(fileMenu);

        insertMenu.setText("Insert");

        jMenu1.setText("Variables");

        jMenuItem2.setText("$datetime");
        jMenuItem2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem2ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem2);

        jMenuItem3.setText("$daylight");
        jMenuItem3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem3ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem3);

        jMenuItem4.setText("$time");
        jMenuItem4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem4ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem4);

        jMenuItem5.setText("$gmtime");
        jMenuItem5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem5ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem5);

        jMenuItem6.setText("$map");
        jMenuItem6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem6ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem6);

        jMenuItem7.setText("$me");
        jMenuItem7.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem7ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem7);

        jMenuItem8.setText("$mynick");
        jMenuItem8.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem8ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem8);

        jMenuItem9.setText("$timezone");
        jMenuItem9.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem9ActionPerformed(evt);
            }
        });
        jMenu1.add(jMenuItem9);

        insertMenu.add(jMenu1);

        jMenu2.setText("Commands");

        jMenuItem11.setText("/auto");
        jMenuItem11.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem11ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem11);

        jMenuItem12.setText("/autoserver");
        jMenuItem12.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem12ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem12);

        jMenuItem13.setText("/automap");
        jMenuItem13.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem13ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem13);

        jMenuItem14.setText("/clear");
        jMenuItem14.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem14ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem14);

        jMenuItem15.setText("/com");
        jMenuItem15.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem15ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem15);

        jMenuItem16.setText("/exit");
        jMenuItem16.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem16ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem16);

        jMenuItem17.setText("/launchserver");
        jMenuItem17.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem17ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem17);

        jMenuItem18.setText("/loadcolours");
        jMenuItem18.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem18ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem18);

        jMenuItem19.setText("/list");
        jMenuItem19.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem19ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem19);

        jMenuItem20.setText("/quit");
        jMenuItem20.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem20ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem20);

        jMenuItem21.setText("/refreshlog");
        jMenuItem21.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem21ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem21);

        jMenuItem22.setText("/stopauto");
        jMenuItem22.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem22ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem22);

        jMenuItem23.setText("/stopautoserver");
        jMenuItem23.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem23ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem23);

        jMenuItem24.setText("/stopautomap");
        jMenuItem24.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem24ActionPerformed(evt);
            }
        });
        jMenu2.add(jMenuItem24);

        insertMenu.add(jMenu2);

        menu.add(insertMenu);

        yspsMenu.setText("YSPS");

        jMenu3.setText("Admin");

        jMenuItem26.setText("/ban (string)username");
        jMenuItem26.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem26ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem26);

        jMenuItem27.setText("/blackout_off");
        jMenuItem27.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem27ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem27);

        jMenuItem28.setText("/blackout_on");
        jMenuItem28.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem28ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem28);

        jMenuItem29.setText("/collisions_off");
        jMenuItem29.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem29ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem29);

        jMenuItem30.setText("/collisions_on");
        jMenuItem30.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem30ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem30);

        jMenuItem31.setText("/day");
        jMenuItem31.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem31ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem31);

        jMenuItem32.setText("/dispell (string)username");
        jMenuItem32.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem32ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem32);

        jMenuItem33.setText("/flushUsers");
        jMenuItem33.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem33ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem33);

        jMenuItem34.setText("/kill_id (number)ID");
        jMenuItem34.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem34ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem34);

        jMenuItem35.setText("/kill_user (string) username");
        jMenuItem35.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem35ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem35);

        jMenuItem36.setText("/landev_off");
        jMenuItem36.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem36ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem36);

        jMenuItem37.setText("/landev_on");
        jMenuItem37.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem37ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem37);

        jMenuItem38.setText("/night");
        jMenuItem38.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem38ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem38);

        jMenuItem39.setText("/radaralti=nuber in meters");
        jMenuItem39.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem39ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem39);

        jMenuItem40.setText("/visib=number in meters");
        jMenuItem40.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem40ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem40);

        jMenuItem41.setText("/windy=number in m/s");
        jMenuItem41.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem41ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem41);

        jMenuItem42.setText("/windx=number in m/s");
        jMenuItem42.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem42ActionPerformed(evt);
            }
        });
        jMenu3.add(jMenuItem42);

        yspsMenu.add(jMenu3);

        jMenu4.setText("All users");

        jMenuItem44.setText("/distance");
        jMenuItem44.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem44ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem44);

        jMenuItem45.setText("/fuel");
        jMenuItem45.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem45ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem45);

        jMenuItem46.setText("/kills");
        jMenuItem46.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem46ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem46);

        jMenuItem47.setText("/listuser");
        jMenuItem47.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem47ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem47);

        jMenuItem48.setText("/lives");
        jMenuItem48.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem48ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem48);

        jMenuItem49.setText("/metar");
        jMenuItem49.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem49ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem49);

        jMenuItem50.setText("/ping");
        jMenuItem50.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem50ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem50);

        jMenuItem51.setText("/pswd%=(string)password");
        jMenuItem51.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem51ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem51);

        jMenuItem52.setText("/reset_info");
        jMenuItem52.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem52ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem52);

        jMenuItem53.setText("/version");
        jMenuItem53.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jMenuItem53ActionPerformed(evt);
            }
        });
        jMenu4.add(jMenuItem53);

        yspsMenu.add(jMenu4);

        menu.add(yspsMenu);

        helpMenu.setText("Help");

        aboutItem.setText("About");
        aboutItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                aboutItemActionPerformed(evt);
            }
        });
        helpMenu.add(aboutItem);

        helpItem.setText("Help");
        helpItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                helpItemActionPerformed(evt);
            }
        });
        helpMenu.add(helpItem);

        menu.add(helpMenu);

        YSCgui.setJMenuBar(menu);

        javax.swing.GroupLayout YSCguiLayout = new javax.swing.GroupLayout(YSCgui.getContentPane());
        YSCgui.getContentPane().setLayout(YSCguiLayout);
        YSCguiLayout.setHorizontalGroup(
            YSCguiLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(YSCguiLayout.createSequentialGroup()
                .addComponent(topPanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGap(10, 10, 10))
            .addComponent(splitPane, javax.swing.GroupLayout.DEFAULT_SIZE, 782, Short.MAX_VALUE)
        );
        YSCguiLayout.setVerticalGroup(
            YSCguiLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(YSCguiLayout.createSequentialGroup()
                .addComponent(topPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(splitPane, javax.swing.GroupLayout.DEFAULT_SIZE, 461, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(YSCgui, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(YSCgui, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
        );

        try {
            YSCgui.setMaximum(true);
        } catch (java.beans.PropertyVetoException e1) {
            e1.printStackTrace();
        }
    }// </editor-fold>//GEN-END:initComponents

    private void connectButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_connectButtonActionPerformed
        connect();
}//GEN-LAST:event_connectButtonActionPerformed

    private void disconnButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disconnButtonActionPerformed
        disconnect();
}//GEN-LAST:event_disconnButtonActionPerformed

    private void servInfoActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_servInfoActionPerformed
        try {
            java.awt.Desktop desktop = java.awt.Desktop.getDesktop();
            java.net.URI uri = new java.net.URI("http://www.yspilots.com/shadowhunters/get_info.php?ip="+ipBox.getSelectedItem()+"&port="+portBox.getText());
            desktop.browse(uri);
        } catch (Exception ex) {}
}//GEN-LAST:event_servInfoActionPerformed

    private void messInKeyReleased(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_messInKeyReleased
        if (evt.getKeyText(evt.getKeyCode()).equals("Enter")) {
            if (messIn.getText().equals("/list")) {
                try {yschat.listPlayers();} catch (IOException ex) {System.out.println("Error getting player list!\t" + ex);}
            } else if (yschat.connected) {
                Date date = new Date();
                messIn.setText(messIn.getText().replace("$mynick", "(" + userBox.getText() + ")"));
                messIn.setText(messIn.getText().replace("$me", userBox.getText()));
                messIn.setText(messIn.getText().replace("$gmtime", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date)));
                messIn.setText(messIn.getText().replace("$datetime", new SimpleDateFormat("E, dd M yyyy HH:mm:ss").format(date)));
                messIn.setText(messIn.getText().replace("$daylight", ""));
                messIn.setText(messIn.getText().replace("$map", mapBox.getText()));
                messIn.setText(messIn.getText().replace("$timezone", new SimpleDateFormat("zzz").format(date)));
                messIn.setText(messIn.getText().replace("$time", new SimpleDateFormat("HH:mm:ss").format(date)));
                try {
                    yschat.sendMess(messIn.getText());
                } catch (IOException ex) {
                    disconnect();
                    JOptionPane.showMessageDialog(this, "Cannot send message. Disconnected from server.", "YS_chat", JOptionPane.ERROR_MESSAGE);
                }
            }
            messIn.setText("");
        }
}//GEN-LAST:event_messInKeyReleased

    private void connectItemconnectButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_connectItemconnectButtonActionPerformed
        connect();
}//GEN-LAST:event_connectItemconnectButtonActionPerformed

    private void disconnItemdisconnButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_disconnItemdisconnButtonActionPerformed
        disconnect();
}//GEN-LAST:event_disconnItemdisconnButtonActionPerformed

    private void servListActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_servListActionPerformed
        try {
            java.awt.Desktop desktop = java.awt.Desktop.getDesktop();
            java.net.URI uri = new java.net.URI("http://www.yspilots.com/shadowhunters/ysServerlist.php");
            desktop.browse(uri);
        } catch (Exception ex) {}
}//GEN-LAST:event_servListActionPerformed

    private void exitItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_exitItemActionPerformed
        System.exit(0);
}//GEN-LAST:event_exitItemActionPerformed

    private void jMenuItem2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem2ActionPerformed
        messIn.setText(messIn.getText()+"$datetime ");
}//GEN-LAST:event_jMenuItem2ActionPerformed

    private void jMenuItem3ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem3ActionPerformed
        messIn.setText(messIn.getText()+"$daylight ");
}//GEN-LAST:event_jMenuItem3ActionPerformed

    private void jMenuItem4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem4ActionPerformed
        messIn.setText(messIn.getText()+"$time ");
}//GEN-LAST:event_jMenuItem4ActionPerformed

    private void jMenuItem5ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem5ActionPerformed
        messIn.setText(messIn.getText()+"$gmtime ");
}//GEN-LAST:event_jMenuItem5ActionPerformed

    private void jMenuItem6ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem6ActionPerformed
        messIn.setText(messIn.getText()+"$map ");
}//GEN-LAST:event_jMenuItem6ActionPerformed

    private void jMenuItem7ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem7ActionPerformed
        messIn.setText(messIn.getText()+"$me ");
}//GEN-LAST:event_jMenuItem7ActionPerformed

    private void jMenuItem8ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem8ActionPerformed
        messIn.setText(messIn.getText()+"$mynick ");
}//GEN-LAST:event_jMenuItem8ActionPerformed

    private void jMenuItem9ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem9ActionPerformed
        messIn.setText(messIn.getText()+"$timezone ");
}//GEN-LAST:event_jMenuItem9ActionPerformed

    private void jMenuItem11ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem11ActionPerformed
        messIn.setText(messIn.getText()+"/auto <5>");
}//GEN-LAST:event_jMenuItem11ActionPerformed

    private void jMenuItem12ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem12ActionPerformed
        messIn.setText(messIn.getText()+"/autoserver");
}//GEN-LAST:event_jMenuItem12ActionPerformed

    private void jMenuItem13ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem13ActionPerformed
        messIn.setText(messIn.getText()+"/automap");
}//GEN-LAST:event_jMenuItem13ActionPerformed

    private void jMenuItem14ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem14ActionPerformed
        messIn.setText(messIn.getText()+"/clear");
}//GEN-LAST:event_jMenuItem14ActionPerformed

    private void jMenuItem15ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem15ActionPerformed
        messIn.setText(messIn.getText()+"/com");
}//GEN-LAST:event_jMenuItem15ActionPerformed

    private void jMenuItem16ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem16ActionPerformed
        messIn.setText(messIn.getText()+"/exit");
}//GEN-LAST:event_jMenuItem16ActionPerformed

    private void jMenuItem17ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem17ActionPerformed
        messIn.setText(messIn.getText()+"/launchserver");
}//GEN-LAST:event_jMenuItem17ActionPerformed

    private void jMenuItem18ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem18ActionPerformed
        messIn.setText(messIn.getText()+"/loadcolours");
}//GEN-LAST:event_jMenuItem18ActionPerformed

    private void jMenuItem19ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem19ActionPerformed
        messIn.setText(messIn.getText()+"/list");
}//GEN-LAST:event_jMenuItem19ActionPerformed

    private void jMenuItem20ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem20ActionPerformed
        messIn.setText(messIn.getText()+"/quit");
}//GEN-LAST:event_jMenuItem20ActionPerformed

    private void jMenuItem21ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem21ActionPerformed
        messIn.setText(messIn.getText()+"/refreshlog");
}//GEN-LAST:event_jMenuItem21ActionPerformed

    private void jMenuItem22ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem22ActionPerformed
        messIn.setText(messIn.getText()+"/stopauto");
}//GEN-LAST:event_jMenuItem22ActionPerformed

    private void jMenuItem23ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem23ActionPerformed
        messIn.setText(messIn.getText()+"/stopautoserver");
}//GEN-LAST:event_jMenuItem23ActionPerformed

    private void jMenuItem24ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem24ActionPerformed
        messIn.setText(messIn.getText()+"/stopautomap");
}//GEN-LAST:event_jMenuItem24ActionPerformed

    private void jMenuItem26ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem26ActionPerformed
        messIn.setText(messIn.getText()+"/blackout_on");
}//GEN-LAST:event_jMenuItem26ActionPerformed

    private void jMenuItem27ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem27ActionPerformed
        messIn.setText(messIn.getText()+"/day");
}//GEN-LAST:event_jMenuItem27ActionPerformed

    private void jMenuItem28ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem28ActionPerformed
        messIn.setText(messIn.getText()+"/landev_on");
}//GEN-LAST:event_jMenuItem28ActionPerformed

    private void jMenuItem29ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem29ActionPerformed
        messIn.setText(messIn.getText()+"/kill_id");
}//GEN-LAST:event_jMenuItem29ActionPerformed

    private void jMenuItem30ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem30ActionPerformed
        messIn.setText(messIn.getText()+"/collisions_off");
}//GEN-LAST:event_jMenuItem30ActionPerformed

    private void jMenuItem31ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem31ActionPerformed
        messIn.setText(messIn.getText()+"/night");
}//GEN-LAST:event_jMenuItem31ActionPerformed

    private void jMenuItem32ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem32ActionPerformed
        messIn.setText(messIn.getText()+"/kill_user");
}//GEN-LAST:event_jMenuItem32ActionPerformed

    private void jMenuItem33ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem33ActionPerformed
        messIn.setText(messIn.getText()+"/windy=");
}//GEN-LAST:event_jMenuItem33ActionPerformed

    private void jMenuItem34ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem34ActionPerformed
        messIn.setText(messIn.getText()+"/visib=");
}//GEN-LAST:event_jMenuItem34ActionPerformed

    private void jMenuItem35ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem35ActionPerformed
        messIn.setText(messIn.getText()+"/collisions_on");
}//GEN-LAST:event_jMenuItem35ActionPerformed

    private void jMenuItem36ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem36ActionPerformed
        messIn.setText(messIn.getText()+"/radaralti=");
}//GEN-LAST:event_jMenuItem36ActionPerformed

    private void jMenuItem37ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem37ActionPerformed
        messIn.setText(messIn.getText()+"/ban");
}//GEN-LAST:event_jMenuItem37ActionPerformed

    private void jMenuItem38ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem38ActionPerformed
        messIn.setText(messIn.getText()+"/dispell");
}//GEN-LAST:event_jMenuItem38ActionPerformed

    private void jMenuItem39ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem39ActionPerformed
        messIn.setText(messIn.getText()+"/windx=");
}//GEN-LAST:event_jMenuItem39ActionPerformed

    private void jMenuItem40ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem40ActionPerformed
        messIn.setText(messIn.getText()+"/blackout_off");
}//GEN-LAST:event_jMenuItem40ActionPerformed

    private void jMenuItem41ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem41ActionPerformed
        messIn.setText(messIn.getText()+"/landev_off");
}//GEN-LAST:event_jMenuItem41ActionPerformed

    private void jMenuItem42ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem42ActionPerformed
        messIn.setText(messIn.getText()+"/flushUsers");
}//GEN-LAST:event_jMenuItem42ActionPerformed

    private void jMenuItem44ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem44ActionPerformed
        messIn.setText(messIn.getText()+"/distance");
}//GEN-LAST:event_jMenuItem44ActionPerformed

    private void jMenuItem45ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem45ActionPerformed
        messIn.setText(messIn.getText()+"/fuel");
}//GEN-LAST:event_jMenuItem45ActionPerformed

    private void jMenuItem46ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem46ActionPerformed
        messIn.setText(messIn.getText()+"/kills");
}//GEN-LAST:event_jMenuItem46ActionPerformed

    private void jMenuItem47ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem47ActionPerformed
        messIn.setText(messIn.getText()+"/listuser");
}//GEN-LAST:event_jMenuItem47ActionPerformed

    private void jMenuItem48ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem48ActionPerformed
        messIn.setText(messIn.getText()+"/lives");
}//GEN-LAST:event_jMenuItem48ActionPerformed

    private void jMenuItem49ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem49ActionPerformed
        messIn.setText(messIn.getText()+"/metar");
}//GEN-LAST:event_jMenuItem49ActionPerformed

    private void jMenuItem50ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem50ActionPerformed
        messIn.setText(messIn.getText()+"/ping");
}//GEN-LAST:event_jMenuItem50ActionPerformed

    private void jMenuItem51ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem51ActionPerformed
        messIn.setText(messIn.getText()+"/pswd%=");
}//GEN-LAST:event_jMenuItem51ActionPerformed

    private void jMenuItem52ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem52ActionPerformed
        messIn.setText(messIn.getText()+"/reset_info");
}//GEN-LAST:event_jMenuItem52ActionPerformed

    private void jMenuItem53ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jMenuItem53ActionPerformed
        messIn.setText(messIn.getText()+"/version");
}//GEN-LAST:event_jMenuItem53ActionPerformed

    private void aboutItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_aboutItemActionPerformed
        about.setSize(320, 130);
        about.setVisible(true);
}//GEN-LAST:event_aboutItemActionPerformed

    private void helpItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_helpItemActionPerformed
        try {
            java.awt.Desktop desktop = java.awt.Desktop.getDesktop();
            java.net.URI uri = new java.net.URI("http://www.yspilots.com/shadowhunters/yschat/doc_yschat.pdf");
            desktop.browse(uri);
        } catch (Exception ex) {}
}//GEN-LAST:event_helpItemActionPerformed
/*
$datetime
$daylight
$time
$gmtime
$map
$me
$mynick
$timezone

/auto <5>
/autoserver
/automap
/clear
/com
/exit
/launchserver
/loadcolours
/list
/quit
/refreshlog
/stopauto
/stopautoserver
/stopautomap

/ban
/blackout_off
/blackout_on
/collisions_off
/collisions_on
/day
/dispell
/flushUsers
/kill_id
/kill_user
/landev_off
/landev_on
/night
/radaralti=
/visib=
/windy=
/windx=

/distance
/fuel
/kills
/listuser
/lives
/metar
/ping
/pswd%=
/reset_info
/version
*/
    public void init() {
        try {
            java.awt.EventQueue.invokeLater(new Runnable() {
                public void run() {
                    new YSC_applet().setVisible(true);
                }
            });
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JInternalFrame YSCgui;
    private javax.swing.JDialog about;
    private javax.swing.JMenuItem aboutItem;
    private javax.swing.JCheckBox automap;
    private javax.swing.JCheckBox automess;
    private javax.swing.JCheckBox autoserver;
    private javax.swing.JButton connectButton;
    private javax.swing.JMenuItem connectItem;
    private javax.swing.JButton disconnButton;
    private javax.swing.JMenuItem disconnItem;
    private javax.swing.JMenuItem exitItem;
    private javax.swing.JMenu fileMenu;
    private javax.swing.JMenuItem helpItem;
    private javax.swing.JMenu helpMenu;
    private javax.swing.JMenu insertMenu;
    private javax.swing.JComboBox ipBox;
    private javax.swing.JMenu jMenu1;
    private javax.swing.JMenu jMenu2;
    private javax.swing.JMenu jMenu3;
    private javax.swing.JMenu jMenu4;
    private javax.swing.JMenuItem jMenuItem11;
    private javax.swing.JMenuItem jMenuItem12;
    private javax.swing.JMenuItem jMenuItem13;
    private javax.swing.JMenuItem jMenuItem14;
    private javax.swing.JMenuItem jMenuItem15;
    private javax.swing.JMenuItem jMenuItem16;
    private javax.swing.JMenuItem jMenuItem17;
    private javax.swing.JMenuItem jMenuItem18;
    private javax.swing.JMenuItem jMenuItem19;
    private javax.swing.JMenuItem jMenuItem2;
    private javax.swing.JMenuItem jMenuItem20;
    private javax.swing.JMenuItem jMenuItem21;
    private javax.swing.JMenuItem jMenuItem22;
    private javax.swing.JMenuItem jMenuItem23;
    private javax.swing.JMenuItem jMenuItem24;
    private javax.swing.JMenuItem jMenuItem26;
    private javax.swing.JMenuItem jMenuItem27;
    private javax.swing.JMenuItem jMenuItem28;
    private javax.swing.JMenuItem jMenuItem29;
    private javax.swing.JMenuItem jMenuItem3;
    private javax.swing.JMenuItem jMenuItem30;
    private javax.swing.JMenuItem jMenuItem31;
    private javax.swing.JMenuItem jMenuItem32;
    private javax.swing.JMenuItem jMenuItem33;
    private javax.swing.JMenuItem jMenuItem34;
    private javax.swing.JMenuItem jMenuItem35;
    private javax.swing.JMenuItem jMenuItem36;
    private javax.swing.JMenuItem jMenuItem37;
    private javax.swing.JMenuItem jMenuItem38;
    private javax.swing.JMenuItem jMenuItem39;
    private javax.swing.JMenuItem jMenuItem4;
    private javax.swing.JMenuItem jMenuItem40;
    private javax.swing.JMenuItem jMenuItem41;
    private javax.swing.JMenuItem jMenuItem42;
    private javax.swing.JMenuItem jMenuItem44;
    private javax.swing.JMenuItem jMenuItem45;
    private javax.swing.JMenuItem jMenuItem46;
    private javax.swing.JMenuItem jMenuItem47;
    private javax.swing.JMenuItem jMenuItem48;
    private javax.swing.JMenuItem jMenuItem49;
    private javax.swing.JMenuItem jMenuItem5;
    private javax.swing.JMenuItem jMenuItem50;
    private javax.swing.JMenuItem jMenuItem51;
    private javax.swing.JMenuItem jMenuItem52;
    private javax.swing.JMenuItem jMenuItem53;
    private javax.swing.JMenuItem jMenuItem6;
    private javax.swing.JMenuItem jMenuItem7;
    private javax.swing.JMenuItem jMenuItem8;
    private javax.swing.JMenuItem jMenuItem9;
    private javax.swing.JOptionPane jOptionPane1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JPopupMenu.Separator jSeparator1;
    private javax.swing.JPanel leftPane;
    private javax.swing.JTextField mapBox;
    private javax.swing.JLabel mapLabel;
    private javax.swing.JMenuBar menu;
    private javax.swing.JTextField messIn;
    public static javax.swing.JEditorPane messOut;
    private javax.swing.JScrollPane messScroll;
    public static javax.swing.JTable playerList;
    private javax.swing.JLabel playersLabel;
    private javax.swing.JTextField portBox;
    private javax.swing.JPanel rightPane;
    private javax.swing.JButton servInfo;
    private javax.swing.JMenuItem servList;
    private javax.swing.JTextField servernameBox;
    private javax.swing.JSplitPane splitPane;
    private javax.swing.JPanel topPanel;
    private javax.swing.JTextField userBox;
    private javax.swing.JTextField versionBox;
    private javax.swing.JMenu yspsMenu;
    // End of variables declaration//GEN-END:variables
}