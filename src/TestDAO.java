import dao.CustomerDAO;
import model.Customer;

public class TestDAO {

    public static void main(String[] args) {

        try {

            Customer customer = new Customer(
                    "Gokul",
                    "9876543210",
                    "gokul@gmail.com"
            );

            CustomerDAO dao = new CustomerDAO();

            int id = dao.addCustomer(customer);

            System.out.println(
                    "Customer added successfully. ID = " + id
            );

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}