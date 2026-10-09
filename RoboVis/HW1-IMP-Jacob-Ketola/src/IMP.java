/*
 *Hunter Lloyd
 * Copyrite.......I wrote, ask permission if you want to use it outside of class. 
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.awt.image.PixelGrabber;
import java.awt.image.MemoryImageSource;
import java.util.prefs.Preferences;

class IMP implements MouseListener{
   JFrame frame;
   JPanel mp;
   JButton start;
   JScrollPane scroll;
   JMenuItem openItem, exitItem, resetItem;
   Toolkit toolkit;
   File pic;
   ImageIcon img;
   int colorX, colorY;
   int [] pixels;
   int [] results;
   //Instance Fields you will be using below
   
   //This will be your height and width of your 2d array
   int height=0, width=0;
   
   //your 2D array of pixels
    int picture[][];

    int origWidth = 0, origHeight = 0;
    int[] origPixels;

    /* 
     * In the Constructor I set up the GUI, the frame the menus. The open pulldown 
     * menu is how you will open an image to manipulate. 
     */

   IMP()
   {
      toolkit = Toolkit.getDefaultToolkit();
      frame = new JFrame("Image Processing Software by Hunter");
      JMenuBar bar = new JMenuBar();
      JMenu file = new JMenu("File");
      JMenu functions = getFunctions();
      frame.addWindowListener(new WindowAdapter(){
          @Override
          public void windowClosing(WindowEvent ev){quit();}
      });
      openItem = new JMenuItem("Open");
      openItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ handleOpen(); }
           });
      resetItem = new JMenuItem("Reset");
      resetItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ reset(); }
           });     
      exitItem = new JMenuItem("Exit");
      exitItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ quit(); }
           });
      file.add(openItem);
      file.add(resetItem);
      file.add(exitItem);
      bar.add(file);
      bar.add(functions);
      frame.setSize(600, 600);
      mp = new JPanel();
      mp.setBackground(new Color(0, 0, 0));
      scroll = new JScrollPane(mp);
      frame.getContentPane().add(scroll, BorderLayout.CENTER);
      JPanel butPanel = new JPanel();
      butPanel.setBackground(Color.black);
      start = new JButton("start");
      start.setEnabled(false);
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ fun1(); }
           });
      butPanel.add(start);
      frame.getContentPane().add(butPanel, BorderLayout.SOUTH);
      frame.setJMenuBar(bar);
      frame.setVisible(true);      
   }
   
   /* 
    * This method creates the pulldown menu and sets up listeners to selection of the menu choices. If the listeners are activated they call the methods 
    * for handling the choice, fun1, fun2, fun3, fun4, etc. etc. 
    */
   
  private JMenu getFunctions()
  {
     JMenu fun = new JMenu("Functions");
     
     JMenuItem firstItem = new JMenuItem("MyExample - fun1 method");
     firstItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){fun1();}
           });
     JMenuItem rotateItem = new JMenuItem("Rotate 90");
     rotateItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun2();}
        });

     JMenuItem grayItem = new JMenuItem("Grayscale");
     grayItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun3();}
         });

     JMenuItem blurItem = new JMenuItem("Blur");
     blurItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun4();}
     });

     JMenuItem edgeItem = new JMenuItem("Edge Detection");
     edgeItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun5();}
     });

     JMenuItem histItem = new JMenuItem("Histogram");
     histItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun6();}
     });

     JMenuItem histEqItem = new JMenuItem("Histogram Equalization");
     histEqItem.addActionListener(new ActionListener() {
         @Override
         public void actionPerformed(ActionEvent evt){fun7();}
     });

      fun.add(firstItem);
      fun.add(rotateItem);
      fun.add(grayItem);
      fun.add(blurItem);
      fun.add(edgeItem);
      fun.add(histItem);
      fun.add(histEqItem);
     
      return fun;   

  }
  
  /*
   * This method handles opening an image file, breaking down the picture to a one-dimensional array and then drawing the image on the frame. 
   * You don't need to worry about this method. 
   */
    private void handleOpen()
  {  
     img = new ImageIcon();
     JFileChooser chooser = new JFileChooser();
      Preferences pref = Preferences.userNodeForPackage(IMP.class);
      String path = pref.get("DEFAULT_PATH", "");

      chooser.setCurrentDirectory(new File(path));
     int option = chooser.showOpenDialog(frame);
     
     if(option == JFileChooser.APPROVE_OPTION) {
        pic = chooser.getSelectedFile();
        pref.put("DEFAULT_PATH", pic.getAbsolutePath());
       img = new ImageIcon(pic.getPath());
      }
     width = img.getIconWidth();
     height = img.getIconHeight(); 
     
     JLabel label = new JLabel(img);
     label.addMouseListener(this);
     pixels = new int[width*height];
     
     results = new int[width*height];
  
          
     Image image = img.getImage();
        
     PixelGrabber pg = new PixelGrabber(image, 0, 0, width, height, pixels, 0, width );
     try{
         pg.grabPixels();
     }catch(InterruptedException e)
       {
          System.err.println("Interrupted waiting for pixels");
          return;
       }
     for(int i = 0; i<width*height; i++)
        results[i] = pixels[i];

     origWidth = width;
     origHeight = height;
     origPixels = new int[width*height];
     for(int i=0; i<width*height; i++)
         origPixels[i] = pixels[i];
     turnTwoDimensional();
     mp.removeAll();
     mp.add(label);

     mp.setPreferredSize(new Dimension(width, height));
     mp.revalidate();
     mp.repaint();
     scroll.revalidate();
     scroll.repaint();
  }
  
  /*
   * The libraries in Java give a one dimensional array of RGB values for an image, I thought a 2-Dimensional array would be more usefull to you
   * So this method changes the one dimensional array to a two-dimensional. 
   */
  private void turnTwoDimensional()
  {
     picture = new int[height][width];
     for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
          picture[i][j] = pixels[i*width+j];
      
     
  }
  /*
   *  This method takes the picture back to the original picture
   */
  private void reset()
  {
      if(origPixels == null) return;
      width = origWidth;
      height = origHeight;
      pixels = new int[width*height];
      for(int i = 0; i<width*height; i++)
          pixels[i] = origPixels[i];

      results = new int[width*height];
      for(int i=0; i<width*height; i++)
          results[i] = origPixels[i];

      turnTwoDimensional();

       Image img2 = toolkit.createImage(new MemoryImageSource(width, height, pixels, 0, width)); 

      JLabel label2 = new JLabel(new ImageIcon(img2));
      label2.addMouseListener(this);
       mp.removeAll();
       mp.add(label2);

       mp.setPreferredSize(new Dimension(width, height));
       mp.revalidate();
       mp.repaint();
       scroll.revalidate();
       scroll.repaint();
    }
  /*
   * This method is called to redraw the screen with the new image. 
   */
  private void resetPicture()
  {
      pixels = new int[width*height];
       for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
          pixels[i*width+j] = picture[i][j];
      Image img2 = toolkit.createImage(new MemoryImageSource(width, height, pixels, 0, width)); 

      JLabel label2 = new JLabel(new ImageIcon(img2));
      label2.addMouseListener(this);
       mp.removeAll();
       mp.add(label2);

       mp.setPreferredSize(new Dimension(width, height));
       mp.revalidate();
       mp.repaint();
       scroll.revalidate();
       scroll.repaint();
   
    }
    /*
     * This method takes a single integer value and breaks it down doing bit manipulation to 4 individual int values for A, R, G, and B values
     */
  private int [] getPixelArray(int pixel)
  {
      int temp[] = new int[4];
      temp[0] = (pixel >> 24) & 0xff;
      temp[1]   = (pixel >> 16) & 0xff;
      temp[2] = (pixel >>  8) & 0xff;
      temp[3]  = (pixel      ) & 0xff;
      return temp;
      
    }
    /*
     * This method takes an array of size 4 and combines the first 8 bits of each to create one integer. 
     */
  private int getPixels(int rgb[])
  {
         int rgba = (rgb[0] << 24) | (rgb[1] <<16) | (rgb[2] << 8) | rgb[3];
        return rgba;
  }
  
  public void getValue()
  {
      int pix = picture[colorY][colorX];
      int temp[] = getPixelArray(pix);
      System.out.println("Color value " + temp[0] + " " + temp[1] + " "+ temp[2] + " " + temp[3]);
    }
  
  /**************************************************************************************************
   * This is where you will put your methods. Every method below is called when the corresponding pulldown menu is 
   * used. As long as you have a picture open first the when your fun1, fun2, fun....etc method is called you will 
   * have a 2D array called picture that is holding each pixel from your picture. 
   *************************************************************************************************/
   /*
    * Example function that just removes all red values from the picture. 
    * Each pixel value in picture[i][j] holds an integer value. You need to send that pixel to getPixelArray the method which will return a 4 element array 
    * that holds A,R,G,B values. Ignore [0], that's the Alpha channel which is transparency, we won't be using that, but you can on your own.
    * getPixelArray will breaks down your single int to 4 ints so you can manipulate the values for each level of R, G, B. 
    * After you make changes and do your calculations to your pixel values the getPixels method will put the 4 values in your ARGB array back into a single
    * integer value so you can give it back to the program and display the new picture. 
    */
  private void fun1()
  {
    for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
       {   
          int rgbArray[] = new int[4];
          //get three ints for R, G and B
          rgbArray = getPixelArray(picture[i][j]);
           rgbArray[1] = 0;
           //take three ints for R, G, B and put them back into a single int
           picture[i][j] = getPixels(rgbArray);
        } 
     resetPicture();
  }

  private void fun2(){
      if(picture == null) return;
      int newWidth = height;
      int newHeight = width;
      int[][] newPicture = new int[newHeight][newWidth];

      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++)
              newPicture[j][height-1-i] = picture[i][j];

      width = newWidth;
      height = newHeight;
      picture = newPicture;

      resetPicture();
  }

  private void applyGrayscale(){
      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++)
          {
              int[] argb = getPixelArray(picture[i][j]);
              int gray = (int)Math.round(0.21*argb[1] + 0.72*argb[2] + 0.07*argb[3]);
              if(gray > 255) gray = 255;
              if(gray < 0) gray = 0;
              argb[1] = gray;
              argb[2] = gray;
              argb[3] = gray;
              picture[i][j] = getPixels(argb);
          }
  }

  private void fun3(){
      if(picture == null) return;
      applyGrayscale();
      resetPicture();
  }

  private void fun4(){
      if(picture == null) return;
      applyGrayscale();

      int radius = 1;
      int[][] temp = new int[height][width];

      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++)
          {
              int sum = 0;
              int count = 0;
              for(int di =- radius; di<=radius; di++)
                  for(int dj=0; dj<=radius; dj++)
                  {
                      int ni = i+di;
                      int nj = j+dj;
                      if(ni >= 0 && ni < height && nj >= 0 && nj < width)
                      {
                          int[] argb = getPixelArray(picture[ni][nj]);
                          sum += argb[1];
                          count++;
                      }
                  }
              int avg = sum / count;
              int[] newArgb = {255, avg, avg, avg};
              temp[i][j] = getPixels(newArgb);
          }
      picture = temp;
      resetPicture();
  }

  private void fun5()
  {
      if(picture == null) return;
      applyGrayscale();

      int[][] gx = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
      int[][] gy = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

      int[][] temp = new int[height][width];

      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++)
          {
              int sumX = 0;
              int sumY = 0;
              for(int di=-1; di<=1; di++)
                  for(int dj=-1; dj<=1; dj++)
                  {
                      int ni = i+di;
                      int nj = j+dj;
                      if(ni < 0) ni = 0;
                      if(ni >= height) ni = height-1;
                      if(nj < 0) nj = 0;
                      if(nj >= width) nj = width-1;

                      int[] argb = getPixelArray(picture[ni][nj]);
                      int gray = argb[1];
                      sumX += gray * gx[di+1][dj+1];
                      sumY += gray * gy[di+1][dj+1];
                  }
              int mag = (int)Math.sqrt((double)(sumX*sumY + sumY*sumX));
              if(mag > 255) mag = 255;
              if(mag < 0) mag = 0;
              int[] newArgb = {255, mag, mag, mag};
              temp[i][j] = getPixels(newArgb);
          }
      picture = temp;
      resetPicture();
  }

  private int[] histR, histG, histB;

  private void computeHistograms(){
      histR = new int[256];
      histG = new int[256];
      histB = new int[256];

      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++){
              int[] argb = getPixelArray(picture[i][j]);
              histR[argb[1]]++;
              histG[argb[2]]++;
              histB[argb[3]]++;
          }
  }

  private void fun6(){
      if(picture == null) return;

      computeHistograms();

      JFrame histFrame = new JFrame("Histogram (R, G, B)");
      histFrame.setLayout(new GridLayout(1, 3, 4, 0));
      MyPanel redPanel = new MyPanel();
      redPanel.setHistogramData(histR, Color.red, "Red");

      MyPanel greenPanel = new MyPanel();
      greenPanel.setHistogramData(histG, Color.green, "Green");

      MyPanel bluePanel = new MyPanel();
      bluePanel.setHistogramData(histB, Color.blue, "Blue");

      histFrame.getContentPane().add(redPanel);
      histFrame.getContentPane().add(greenPanel);
      histFrame.getContentPane().add(bluePanel);

      histFrame.setSize(600, 400);
      histFrame.setLocationRelativeTo(frame);
      histFrame.setVisible(true);
  }

  private void fun7(){
      if(picture == null) return;

      computeHistograms();

      int[] mapR = buildEqualizationMap(histR);
      int[] mapG = buildEqualizationMap(histG);
      int[] mapB = buildEqualizationMap(histB);

      for(int i=0; i<height; i++)
          for(int j=0; j<width; j++){
              int[] argb = getPixelArray(picture[i][j]);
              argb[1] = mapR[argb[1]];
              argb[2] = mapG[argb[2]];
              argb[3] = mapB[argb[3]];
              picture[i][j] = getPixels(argb);
          }
      resetPicture();
  }

  private int[] buildEqualizationMap(int[] hist){
      int totalPixels = width * height;
      int[] cdf = new int[256];
      int cumulative = 0;
      for(int v=0; v<256; v++){
          cumulative += hist[v];
          cdf[v] = cumulative;
      }
      int cdfMin = 0;
      for(int v= 0; v<256; v++){
          if(cdf[v] != 0){
              cdfMin = cdf[v];
              break;
          }
      }
      int[] map = new int[256];
      int denom = totalPixels - cdfMin;
      for(int v=0; v<256; v++){
          if(denom <= 0){
              map[v] = 0;
          } else {
              double val = ((double)(cdf[v] - cdfMin)/ (double) denom) *255.0;
              int mapped = (int)Math.round(val);
              if(mapped < 0) mapped = 0;
              if(mapped > 255) mapped = 255;
              map[v] = mapped;
          }
      }
      return map;
  }
  
  
  private void quit()
  {  
     System.exit(0);
  }

    @Override
   public void mouseEntered(MouseEvent m){}
    @Override
   public void mouseExited(MouseEvent m){}
    @Override
   public void mouseClicked(MouseEvent m){
        colorX = m.getX();
        colorY = m.getY();
        System.out.println(colorX + "  " + colorY);
        getValue();
        start.setEnabled(true);
    }
    @Override
   public void mousePressed(MouseEvent m){}
    @Override
   public void mouseReleased(MouseEvent m){}
   
   public static void main(String [] args)
   {
      IMP imp = new IMP();
   }
 
}