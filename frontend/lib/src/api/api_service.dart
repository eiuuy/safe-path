import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  final String baseUrl = "https://safe-path-gaor.onrender.com/api/v1";

  Future<Map<String, String>> _headers() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token') ?? '';
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  // 1. АВТОРИЗАЦИЯ (теперь без роли)
  Future<bool> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({"email": email, "password": password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final prefs = await SharedPreferences.getInstance();

        // Сохраняем токен и роль (если сервер её возвращает)
        await prefs.setString('auth_token', data['access_token']);
        if (data.containsKey('role')) {
          await prefs.setString('user_role', data['role']);
        }
        return true;
      }
      return false;
    } catch (e) {
      print("Ошибка входа: $e");
      return false;
    }
  }

  // 2. РЕГИСТРАЦИЯ (с выбором роли)
  Future<bool> register(String email, String role, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({"email": email, "role": role, "password": password}),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print("Ошибка регистрации: $e");
      return false;
    }
  }

  // Остальные методы (Круги, Позиции, Места) остаются без изменений
  Future<List<dynamic>> getCircles() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/circles/'),
        headers: await _headers(),
      );
      return response.statusCode == 200 ? jsonDecode(response.body) : [];
    } catch (e) {
      return [];
    }
  }

  Future<bool> createCircle(String name) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/circles/'),
        headers: await _headers(),
        body: jsonEncode({"name": name}),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }

  Future<bool> updatePosition(double lat, double lon) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/positions/'),
        headers: await _headers(),
        body: jsonEncode({"latitude": lat, "longitude": lon}),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  Future<dynamic> getNearestSafeSpace(double lat, double lon) async {
    try {
      final url = '$baseUrl/safe-spaces/safe-spaces/nearest?lat=$lat&lon=$lon';
      final response = await http.get(
        Uri.parse(url),
        headers: await _headers(),
      );
      return response.statusCode == 200 ? jsonDecode(response.body) : null;
    } catch (e) {
      return null;
    }
  }
}
