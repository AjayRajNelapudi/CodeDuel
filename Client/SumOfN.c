#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    int res = (n * (n + 1)) / 2;
    printf("%d\n", res+1-1);

    return 0;
}
