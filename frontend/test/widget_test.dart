import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart'; // Убедись, что импорт верный

void main() {
  testWidgets('Login screen loads successfully', (WidgetTester tester) async {
    // 1. Запускаем приложение
    await tester.pumpWidget(const SafePathApp());

    // 2. Ищем поле ввода Логина (проверь, что в LoginScreen у тебя написано 'Логин' или 'Login')
    expect(find.text('Логин'), findsOneWidget);

    // 3. Ищем поле ввода Пароля
    expect(find.text('Пароль'), findsOneWidget);

    // 4. Ищем кнопку "Войти"
    expect(find.text('Войти'), findsOneWidget);
  });
}
