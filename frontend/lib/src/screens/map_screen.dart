import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../api/api_service.dart'; // Убедись, что путь правильный
import '../components/sos_button.dart';
import '../components/safe_info_card.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final LatLng _center = const LatLng(53.2858, 69.4128);
  final ApiService _api = ApiService();

  // Состояния для хранения данных с бэкенда
  List _circles = [];
  String _statusText = "E.C.H.O. Mate: Загрузка...";

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  // Метод для получения данных при запуске
  Future<void> _loadData() async {
    try {
      var data = await _api.getCircles();
      if (mounted) {
        setState(() {
          _circles = data;
          _statusText = "E.C.H.O. Mate: Защищен (${_circles.length} кругов)";
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _statusText = "E.C.H.O. Mate: Ошибка сети");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(target: _center, zoom: 15),
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
          ),

          // Инфо-карточка (теперь она будет менять текст при загрузке данных)
          Positioned(
            top: 60,
            left: 20,
            right: 20,
            child: SafeInfoCard(status: _statusText),
          ),

          // Кнопка SOS
          const Positioned(bottom: 40, right: 30, child: SosButton()),

          // Дополнительно: Кнопка для ручного обновления (если нужно)
          Positioned(
            top: 60,
            right: 20,
            child: FloatingActionButton(
              mini: true,
              onPressed: _loadData,
              child: const Icon(Icons.refresh),
            ),
          ),
        ],
      ),
    );
  }
}
