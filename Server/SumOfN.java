import java.util.Scanner;

class SumOfN {
	public static void main(String args[]) {
		Scanner read = new Scanner(System.in);
		int n = read.nextInt();
		int res = n * ((n + 1) / 2);
		System.out.print(res);
	}
}