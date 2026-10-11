package gui;

import dao.ReservationDAO;
import model.ReservationDetail;
import util.ValidationUtil;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.sql.SQLException;
import java.util.List;

/**
 * Search reservations by ID, customer name or phone number.
 */
public class SearchReservationDialog extends JDialog {

    private static final String BY_ID = "Reservation ID";
    private static final String BY_NAME = "Customer Name";
    private static final String BY_PHONE = "Phone Number";

    private final JComboBox<String> criteriaCombo =
            new JComboBox<>(new String[]{BY_ID, BY_NAME, BY_PHONE});
    private final JTextField searchField = new JTextField(20);
    private final ReservationListPanel listPanel = new ReservationListPanel();
    private final JLabel resultLabel = new JLabel("Enter a search value");

    private final ReservationDAO reservationDAO = new ReservationDAO();

    public SearchReservationDialog(JFrame owner) {
        super(owner, "Search Reservation", true);
        setSize(940, 560);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(760, 420));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("Search Reservation",
                "Search by reservation ID, customer name or phone number"),
                BorderLayout.NORTH);
        add(buildCenter(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        // Enter key triggers the search
        searchField.addActionListener(e -> search());
    }

    private JPanel buildCenter() {
        JPanel center = new JPanel(new BorderLayout(0, 12));
        center.setBackground(GUITheme.BACKGROUND);
        center.setBorder(new EmptyBorder(14, 16, 12, 16));

        // ----- search bar -----
        JPanel searchPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 0));
        searchPanel.setOpaque(false);

        searchPanel.add(GUITheme.label("Search by:"));
        GUITheme.styleCombo(criteriaCombo);
        searchPanel.add(criteriaCombo);

        GUITheme.styleField(searchField);
        searchField.setToolTipText("Type a value and press Enter");
        searchPanel.add(searchField);

        JButton searchButton = GUITheme.button("Search", GUITheme.ACCENT);
        searchButton.addActionListener(e -> search());
        searchPanel.add(searchButton);

        JButton allButton = GUITheme.button("Show All",
                GUITheme.PRIMARY_LIGHT);
        allButton.addActionListener(e -> showAll());
        searchPanel.add(allButton);

        center.add(searchPanel, BorderLayout.NORTH);

        // ----- results -----
        JPanel results = new JPanel(new BorderLayout(0, 6));
        results.setOpaque(false);
        resultLabel.setFont(GUITheme.SMALL);
        resultLabel.setForeground(GUITheme.MUTED);
        results.add(resultLabel, BorderLayout.NORTH);
        results.add(listPanel, BorderLayout.CENTER);

        center.add(results, BorderLayout.CENTER);
        return center;
    }

    private JPanel buildButtonBar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 12));
        bar.setBackground(GUITheme.BACKGROUND);

        JButton close = GUITheme.button("Close", GUITheme.PRIMARY);
        close.addActionListener(e -> dispose());
        bar.add(close);
        return bar;
    }

    private void search() {
        String text = searchField.getText();

        if (ValidationUtil.isBlank(text)) {
            GUITheme.error(this,
                    "Please enter a value to search for.");
            searchField.requestFocus();
            return;
        }

        String criteria = (String) criteriaCombo.getSelectedItem();
        String searchBy;
        String readable;

        if (BY_ID.equals(criteria)) {
            searchBy = ReservationDAO.SEARCH_ID;
            readable = "reservation ID";
        } else if (BY_PHONE.equals(criteria)) {
            searchBy = ReservationDAO.SEARCH_PHONE;
            readable = "phone";
        } else {
            searchBy = ReservationDAO.SEARCH_NAME;
            readable = "name";
        }

        // reservation ID must be a number
        if (ReservationDAO.SEARCH_ID.equals(searchBy)
                && !text.trim().matches("\\d+")) {
            GUITheme.error(this,
                    "Reservation ID must be a whole number.");
            searchField.requestFocus();
            return;
        }

        try {
            List<ReservationDetail> results =
                    reservationDAO.searchReservationDetails(searchBy, text);

            listPanel.setReservations(results);

            if (results.isEmpty()) {
                resultLabel.setText("0 result(s)");
                GUITheme.info(this,
                        "No reservations found for " + readable + ": "
                                + text.trim());
            } else {
                resultLabel.setText(results.size()
                        + " result(s) for " + readable + ": " + text.trim());
            }

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Search failed:\n" + e.getMessage());
        } catch (NumberFormatException e) {
            GUITheme.error(this,
                    "Reservation ID must be a valid whole number.");
        }
    }

    private void showAll() {
        searchField.setText("");
        try {
            List<ReservationDetail> all =
                    reservationDAO.getAllReservationDetails();
            listPanel.setReservations(all);
            resultLabel.setText(all.size() + " reservation(s) total");
        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load reservations:\n" + e.getMessage());
        }
    }
}
