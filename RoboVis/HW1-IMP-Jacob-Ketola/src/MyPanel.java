
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class MyPanel extends JPanel
{
 
int startX, flag, startY, endX, endY;

    BufferedImage grid;
    Graphics2D gc;

    int[] hist;
    Color histColor = Color.white;
    String histLabel = "";
    boolean showHistogram = false;

	public MyPanel()
	{
	   startX = startY = 0;
           endX = endY = 100;
 	}

     public void clear()
    {
       grid = null;
       showHistogram = false;
       repaint();
    }

    public void setHistogramData(int[] hist, Color color, String label){
        this.hist = hist;
        this.histColor = color;
        this.histLabel = label;
        this.showHistogram = true;
        grid = null;
        repaint();
    }

    public void paintComponent(Graphics g)
    {  
         super.paintComponent(g);
         Graphics2D g2 = (Graphics2D)g;
         if(grid == null){
            int w = this.getWidth();
            int h = this.getHeight();
            if(w <= 0) w = 1;
            if(h <= 0) h = 1;
            grid = (BufferedImage)(this.createImage(w,h));
            gc = grid.createGraphics();
            gc.setColor(Color.black);
            gc.fillRect(0, 0, w, h);

            if(showHistogram)
                drawHistogram(w,h);

         }
         g2.drawImage(grid, null, 0, 0);
     }
    public void drawing()
    {
        
        gc.drawLine(startX, startY, endX, endY);
        repaint();
    }

    private void drawHistogram(int w, int h){
        if(hist == null) return;

        int topMargin = 24;
        int margin = 10;
        int usableW = Math.max(1, w - 2*margin);
        int usableH = Math.max(1, h - 2*margin);

        int max = 1;
        for(int v=0; v<256; v++)
            if(hist[v] > max) max = hist[v];

            int baseline = h - margin;
            gc.setColor(histColor);
            for(int v=0; v<256; v++){
                int x = margin + (int)Math.round(v * (usableW / 255.0));
                int barHeight = (int)Math.round(((double)hist[v] / (double)max) * usableH);
                int y1 = baseline;
                int y2 = baseline - barHeight;
                gc.drawLine(x, y1, x, y2);
            }

            gc.setColor(Color.white);
            gc.setFont(gc.getFont().deriveFont(Font.BOLD, 14f));
            gc.drawString(histLabel, margin, 16);
        }

}
