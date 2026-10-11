import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

/** Renders the picker preview image. Run: java tools/RenderPreview.java <out.png> */
public class RenderPreview {
    public static void main(String[] args) throws Exception {
        int s = 450;
        BufferedImage img = new BufferedImage(s, s, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setColor(Color.BLACK);
        g.fill(new Ellipse2D.Double(0, 0, s, s));

        // Date + battery
        String date = "воскресенье 11.10";
        g.setFont(new Font("SansSerif", Font.PLAIN, 30));
        FontMetrics fm = g.getFontMetrics();
        int tw = fm.stringWidth(date), bw = 40, gap = 10;
        int x0 = (s - (tw + gap + bw)) / 2;
        g.setColor(new Color(0xE6E6E6));
        g.drawString(date, x0, 92 + 22 + fm.getAscent() / 2 - 2);
        int bx = x0 + tw + gap, by = 105;
        g.setColor(Color.WHITE);
        g.setStroke(new BasicStroke(2));
        g.draw(new RoundRectangle2D.Double(bx + 1, by + 1, 34, 18, 8, 8));
        g.fill(new RoundRectangle2D.Double(bx + 36, by + 6, 3.5, 8, 3, 3));
        g.fill(new Rectangle2D.Double(bx + 4, by + 4, 28 * 0.8, 12));

        // Time
        g.setFont(new Font("SansSerif", Font.BOLD, 124));
        fm = g.getFontMetrics();
        String t = "10:08";
        g.drawString(t, (s - fm.stringWidth(t)) / 2, 140 + 75 + fm.getAscent() / 2 - 14);

        // Complications
        int d = 90, cy = 296;
        int[] xs = {225 - 8 - d, 225 + 8};
        String[][] labels = {{"3", "УФ"}, {"5:00", "Таймер"}};
        for (int i = 0; i < 2; i++) {
            g.setColor(new Color(0x161616));
            g.fill(new Ellipse2D.Double(xs[i] + 1, cy + 1, d - 2, d - 2));
            g.setColor(new Color(0x3C3C3C));
            g.draw(new Ellipse2D.Double(xs[i] + 1, cy + 1, d - 2, d - 2));
            g.setColor(Color.WHITE);
            g.setFont(new Font("SansSerif", Font.BOLD, 24));
            fm = g.getFontMetrics();
            g.drawString(labels[i][0], xs[i] + (d - fm.stringWidth(labels[i][0])) / 2, cy + 46);
            g.setColor(new Color(0xB0B0B0));
            g.setFont(new Font("SansSerif", Font.PLAIN, 15));
            fm = g.getFontMetrics();
            g.drawString(labels[i][1], xs[i] + (d - fm.stringWidth(labels[i][1])) / 2, cy + 69);
        }
        g.dispose();
        ImageIO.write(img, "png", new File(args[0]));
    }
}
