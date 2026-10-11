package util;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeParseException;
import java.util.regex.Pattern;

/**
 * Central place for all input validation rules so that every screen
 * applies exactly the same checks.
 */
public final class ValidationUtil {

    private static final Pattern PHONE_PATTERN =
            Pattern.compile("^\\+?\\d{10,15}$");

    private static final Pattern EMAIL_PATTERN =
            Pattern.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    private ValidationUtil() {
        // utility class - cannot be instantiated
    }

    public static boolean isBlank(String text) {
        return text == null || text.trim().isEmpty();
    }

    /** Accepts 10-15 digits, optional leading '+', spaces and dashes ignored. */
    public static boolean isValidPhone(String phone) {
        if (isBlank(phone)) {
            return false;
        }
        String cleaned = phone.trim().replace(" ", "").replace("-", "");
        return PHONE_PATTERN.matcher(cleaned).matches();
    }

    public static boolean isValidEmail(String email) {
        if (isBlank(email)) {
            return false;
        }
        return EMAIL_PATTERN.matcher(email.trim()).matches();
    }

    /** Parses a date in ISO format (yyyy-MM-dd). */
    public static LocalDate parseDate(String text)
            throws DateTimeParseException {

        return LocalDate.parse(text.trim());
    }

    /** Parses a time as HH:mm or HH:mm:ss. */
    public static LocalTime parseTime(String text)
            throws DateTimeParseException {

        String value = text.trim();

        if (value.matches("^\\d{1,2}:\\d{2}$")) {
            String[] parts = value.split(":");
            value = String.format("%02d:%s:00",
                    Integer.parseInt(parts[0]), parts[1]);
        }

        return LocalTime.parse(value);
    }

    /** True when the slot is in the past (date before today, or time today already passed). */
    public static boolean isPastSlot(LocalDate date, LocalTime time) {
        LocalDate today = LocalDate.now();
        return date.isBefore(today)
                || (date.isEqual(today) && time.isBefore(LocalTime.now()));
    }

    /** A reservation needs at least one guest and cannot exceed the table capacity. */
    public static boolean isValidGuestCount(int guests, int capacity) {
        return guests > 0 && guests <= capacity;
    }
}
