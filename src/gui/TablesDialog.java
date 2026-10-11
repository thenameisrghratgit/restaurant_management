package gui;

import dao.ReservationDAO;
import dao.TableDAO;
import model.RestaurantTable;
import util.ValidationUtil;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableCellRenderer;
import java.awt.*;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeParseException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Shows every restaurant table and, for a chosen date/time slot, whether
 * each table is free or already booked. Availability is calculated from
 * the reservations table - tables are never permanently marked as busy.
 */
public class TablesDialog extends JDialog {

    private final JTextField dateField = new JTextField(12);
    private final JTextField timeField = new JTextField(8);
    private final JLabel slotLabel =
            GUITheme.label("No time slot selected yet.");

    private final TableDAO tableDAO = new TableDAO();
    private final ReservationDAO reservationDAO = new ReservationDAO();

    private List<RestaurantTable> tables;
    private final Map<Integer, String> availability = new HashMap<>();

    private final TablesTableModel model = new TablesTableModel();
    private final JTable table = new JTable(model);

    public TablesDialog(JFrame owner) {
        super(owner, "Available Tables", true);
        setSize(760, 520);
        setLocationRelativeTo(owner);
        setMinimumSize(new Dimension(640, 400));
        setLayout(new BorderLayout());

        add(GUITheme.dialogHeader("Restaurant Tables",
                "Table status plus live availability for a date/time slot"),
                BorderLayout.NORTH);
        add(buildCenter(), BorderLayout.CENTER);
        add(buildButtonBar(), BorderLayout.SOUTH);

        GUITheme.styleTable(table);
        table.setRowHeight(30);
        slotLabel.setFont(GUITheme.SMALL);
        slotLabel.setForeground(GUITheme.MUTED);

        dateField.setText(LocalDate.now().plusDays(1).toString());
        timeField.setText("19:00");

        loadTables();
    }

    private JPanel buildCenter() {
        JPanel center = new JPanel(new BorderLayout(0, 10));
        center.setBackground(GUITheme.BACKGROUND);
        center.setBorder(new EmptyBorder(12, 16, 8, 16));

        // ----- slot picker (GridBag so the row never wraps) -----
        JPanel picker = new JPanel(new GridBagLayout());
        picker.setOpaque(false);

        GridBagConstraints gc = new GridBagConstraints();
        gc.gridy = 0;
        gc.insets = new Insets(4, 6, 4, 6);
        gc.anchor = GridBagConstraints.WEST;

        gc.gridx = 0;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        picker.add(GUITheme.label("Date (yyyy-MM-dd):"), gc);

        GUITheme.styleField(dateField);
        gc.gridx = 1;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        picker.add(dateField, gc);

        gc.gridx = 2;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        picker.add(GUITheme.label("Time (HH:mm):"), gc);

        GUITheme.styleField(timeField);
        gc.gridx = 3;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        picker.add(timeField, gc);

        JButton check = GUITheme.button("Check Availability", GUITheme.ACCENT);
        check.addActionListener(e -> checkAvailability());
        gc.gridx = 4;
        gc.weightx = 0;
        gc.fill = GridBagConstraints.NONE;
        picker.add(check, gc);

        JButton showAll = GUITheme.button("Show All",
                GUITheme.PRIMARY_LIGHT);
        showAll.addActionListener(e -> {
            availability.clear();
            model.fireTableDataChanged();
            slotLabel.setText("No time slot selected yet.");
        });
        gc.gridx = 5;
        picker.add(showAll, gc);

        center.add(picker, BorderLayout.NORTH);

        // ----- table -----
        JPanel tableArea = new JPanel(new BorderLayout(0, 6));
        tableArea.setOpaque(false);
        tableArea.add(slotLabel, BorderLayout.NORTH);
        tableArea.add(new JScrollPane(table), BorderLayout.CENTER);

        center.add(tableArea, BorderLayout.CENTER);

        applyAvailabilityColumnRenderer();
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

    // ----- green/red text for the availability column -----
    private void applyAvailabilityColumnRenderer() {
        DefaultTableCellRenderer renderer = new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(
                    JTable t, Object value, boolean isSelected,
                    boolean hasFocus, int row, int column) {

                Component c = super.getTableCellRendererComponent(
                        t, value, isSelected, hasFocus, row, column);

                setHorizontalAlignment(SwingConstants.CENTER);

                if (!isSelected) {
                    if ("AVAILABLE".equals(value)) {
                        c.setForeground(GUITheme.SUCCESS);
                        c.setFont(GUITheme.BUTTON);
                    } else if ("OCCUPIED".equals(value)) {
                        c.setForeground(GUITheme.DANGER);
                        c.setFont(GUITheme.BUTTON);
                    } else {
                        c.setForeground(GUITheme.MUTED);
                        c.setFont(GUITheme.BODY);
                    }
                }
                return c;
            }
        };
        table.getColumnModel().getColumn(3).setCellRenderer(renderer);
    }

    // ================================================================
    //  LOGIC
    // ================================================================

    private void loadTables() {
        try {
            tables = tableDAO.getAllTables();
            availability.clear();
            model.fireTableDataChanged();
        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not load tables:\n" + e.getMessage());
        }
    }

    /** Calculates which tables are free for the entered date/time slot. */
    private void checkAvailability() {
        LocalDate date;
        LocalTime time;

        try {
            date = ValidationUtil.parseDate(dateField.getText());
            time = ValidationUtil.parseTime(timeField.getText());
        } catch (DateTimeParseException e) {
            GUITheme.error(this,
                    "Enter a valid date (yyyy-MM-dd) and time (HH:mm) "
                            + "first.");
            return;
        }

        try {
            Set<Integer> bookedIds =
                    reservationDAO.getBookedTableIds(date, time);

            availability.clear();
            if (tables != null) {
                for (RestaurantTable t : tables) {
                    availability.put(t.getTableId(),
                            bookedIds.contains(t.getTableId())
                                    ? "OCCUPIED" : "AVAILABLE");
                }
            }

            model.fireTableDataChanged();

            slotLabel.setText("Availability on " + date + " at "
                    + String.format("%02d:%02d",
                    time.getHour(), time.getMinute())
                    + "  -  free: " + availability.values().stream()
                    .filter("AVAILABLE"::equals).count()
                    + ", occupied: " + bookedIds.size());

        } catch (SQLException e) {
            e.printStackTrace();
            GUITheme.error(this,
                    "Could not check availability:\n" + e.getMessage());
        }
    }

    // ================================================================
    //  TABLE MODEL
    // ================================================================

    private class TablesTableModel extends AbstractTableModel {

        private final String[] columns = {
                "Table Number", "Capacity", "Table Status", "Slot Availability"
        };

        @Override
        public int getRowCount() {
            return tables == null ? 0 : tables.size();
        }

        @Override
        public int getColumnCount() {
            return columns.length;
        }

        @Override
        public String getColumnName(int column) {
            return columns[column];
        }

        @Override
        public Class<?> getColumnClass(int column) {
            return column == 0 || column == 1 ? Integer.class : String.class;
        }

        @Override
        public Object getValueAt(int row, int column) {
            RestaurantTable t = tables.get(row);

            return switch (column) {
                case 0 -> t.getTableNumber();
                case 1 -> t.getCapacity();
                case 2 -> t.getStatus();
                default -> availability.getOrDefault(t.getTableId(),
                        "Enter date & time");
            };
        }
    }
}
