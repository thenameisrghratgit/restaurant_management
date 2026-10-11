package gui;

import model.ReservationDetail;

import javax.swing.table.AbstractTableModel;
import java.util.ArrayList;
import java.util.List;

/**
 * Table model that feeds every reservation JTable in the application.
 * One class, four screens (view, search, modify, cancel) - the columns are
 * always identical.
 */
public class ReservationTableModel extends AbstractTableModel {

    private static final String[] COLUMNS = {
            "ID", "Customer", "Phone", "Table",
            "Guests", "Date", "Time", "Status"
    };

    private List<ReservationDetail> rows = new ArrayList<>();

    public void setRows(List<ReservationDetail> rows) {
        this.rows = (rows == null) ? new ArrayList<>() : rows;
        fireTableDataChanged();
    }

    public ReservationDetail getRow(int modelIndex) {
        return rows.get(modelIndex);
    }

    @Override
    public int getRowCount() {
        return rows.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNS.length;
    }

    @Override
    public String getColumnName(int column) {
        return COLUMNS[column];
    }

    @Override
    public Class<?> getColumnClass(int columnIndex) {
        return switch (columnIndex) {
            case 0, 3, 4 -> Integer.class;
            default -> String.class;
        };
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        ReservationDetail d = rows.get(rowIndex);

        return switch (columnIndex) {
            case 0 -> d.getReservationId();
            case 1 -> d.getCustomerName();
            case 2 -> d.getPhone();
            case 3 -> d.getTableNumber();
            case 4 -> d.getGuests();
            case 5 -> d.getDateText();
            case 6 -> d.getTimeText();
            default -> d.getStatus();
        };
    }
}
