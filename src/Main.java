import gui.MainFrame;
import util.DBConnection;

import javax.swing.*;
import java.sql.Connection;

/**
 * Application entry point: verifies the database connection first,
 * then launches the Swing dashboard on the Event Dispatch Thread.
 */
public class Main {

    public static void main(String[] args) {

        // --- catch unexpected runtime exceptions anywhere in the app ---
        Thread.setDefaultUncaughtExceptionHandler((thread, error) -> {
            error.printStackTrace();
            JOptionPane.showMessageDialog(null,
                    "An unexpected error occurred:\n" + error.getMessage(),
                    "Unexpected Error",
                    JOptionPane.ERROR_MESSAGE);
        });

        // --- JDBC connectivity check before any window opens ---
        try (Connection connection = DBConnection.getConnection()) {
            if (!connection.isValid(3)) {
                throw new java.sql.SQLException(
                        "Connection reported as invalid.");
            }
            System.out.println("Database connected successfully!");
        } catch (Exception e) {
            System.out.println("Database connection failed!");
            e.printStackTrace();

            JOptionPane.showMessageDialog(null,
                    "Could not connect to the database.\n\n"
                            + "Please make sure MySQL is running and try again.\n"
                            + "Details: " + e.getMessage(),
                    "Database Connection Error",
                    JOptionPane.ERROR_MESSAGE);
            return; // do not open the GUI without a database
        }

        // --- Initialize users table & default admin if needed ---
        try {
            new dao.UserDAO().initTable();
        } catch (Exception e) {
            System.err.println("Warning: Could not initialize users table: " + e.getMessage());
        }

        // --- Swing GUI must be created on the Event Dispatch Thread ---
        SwingUtilities.invokeLater(() -> {
            MainFrame mainFrame = new MainFrame();
            mainFrame.setVisible(true);
        });
    }
}
