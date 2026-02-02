import java.util.*;

public class Member extends Person {
    private Loan loan;

    public Member() {}

    public Loan getLoan() {
        return this.loan;
    }

}