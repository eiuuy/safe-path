import 'package:flutter/material.dart';
import '../components/sos_button.dart';
import '../components/safe_info_card.dart';

class TeenagerDashboard extends StatelessWidget {
  const TeenagerDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF9FAFB),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            // ПЕРЕДАЕМ статус здесь:
            const SafeInfoCard(status: "Статус: Все в порядке"),

            const SizedBox(height: 20),
            Expanded(
              child: Row(
                children: [
                  Expanded(
                    flex: 1,
                    child: SosButton(
                      onPressed: () {
                        print("SOS нажата!");
                      },
                    ),
                  ),
                  const SizedBox(width: 20),
                  Expanded(
                    flex: 2,
                    child: Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: const Center(child: Text("Карта")),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
