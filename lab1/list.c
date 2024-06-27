#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define EMPTY_STACK -1

typedef struct Node {
    char data;
    struct Node *next;
} Node;

typedef struct List {
    Node *head;
} List;

void init_link_list(List *list) {
    list->head = NULL;
}

void insert(List *list, char data) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    new_node->data = data;
    new_node->next = NULL;

    if (list->head == NULL) {
        list->head = new_node;
    } else {
        Node *current = list->head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = new_node;
    }
}

void print_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("%c ", current->data);
        current = current->next;
    }
    printf("\n");
}

typedef struct Stack {
    char *items;
    int top;
    int size;
} Stack;

void init_stack(Stack *stack, int size) {
    stack->top = EMPTY_STACK;
    stack->size = size;
    stack->items = (char *)malloc(stack->size * sizeof(char));
}

bool is_empty(Stack *stack) {
    return stack->top == EMPTY_STACK;
}

void push(Stack *stack, char item) {
    if (stack->top == stack->size - 1) {
        printf("Stack is full\n");
        return;
    }

    stack->top++;
    stack->items[stack->top] = item;
}

char pop(Stack *stack) {
    if (is_empty(stack)) {
        return '\0';
    }

    char to_popped = stack->items[stack->top];
    stack->top--;
    return to_popped;
}

char top(Stack *stack) {
    if (is_empty(stack)) {
        return '\0';
    }
    return stack->items[stack->top];
}

void free_list(Node *head) {
    Node *current = head;
    Node *next;
    while (current != NULL) {
        next = current->next;
        free(current);
        current = next;
    }
}

bool is_palindrome(char *string) {
    List list;
    init_link_list(&list);
    Stack stack;
    init_stack(&stack, strlen(string));

    for (int i = 0; string[i] != '\0'; i++) {
        insert(&list, string[i]);
        push(&stack, string[i]);
    }

    Node *current = list.head;
    while (current != NULL) {
        char item = pop(&stack);
        if (item != current->data) {
            free(stack.items);
            free_list(list.head);
            return false;
        }
        current = current->next;
    }

    free(stack.items);
    free_list(list.head);
    return true;
}

int main() {
    char test_string[] = "kaj";

    printf("Is the string a palindrome?\n");
    if (is_palindrome(test_string)) {
        printf("Yes\n");
    } else {
        printf("No\n");
    }
    return 0;
}
