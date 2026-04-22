import 'package:flutter/material.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  // Переменная для выбора роли
  String _selectedRole = 'Teenager';
  final List<String> _roles = ['Teenager', 'Parent', 'Partner'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Регистрация")),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: "Email"),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: "Пароль"),
              obscureText: true,
            ),

            const SizedBox(height: 20),

            // Выбор роли
            DropdownButtonFormField<String>(
              value: _selectedRole,
              decoration: const InputDecoration(
                labelText: "Выберите вашу роль",
              ),
              items: _roles.map((role) {
                return DropdownMenuItem(value: role, child: Text(role));
              }).toList(),
              onChanged: (value) {
                setState(() => _selectedRole = value!);
              },
            ),

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                print("Регистрация пользователя как: $_selectedRole");
                // Здесь будет вызов API
              },
              child: const Text("Зарегистрироваться"),
            ),
          ],
        ),
      ),
    );
  }
}
