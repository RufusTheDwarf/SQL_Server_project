# Audit du dépôt avant refonte

## État général

Le dépôt contenait une première activité d'enquête autour de joueurs suspects, une application Flask et des ressources SQL de formation. Cette activité est conservée dans son emplacement historique. La refonte est développée dans `version-finale/mission-sql-cinema/` sur la branche `refonte-activite-etml`.

## Points réutilisables

- Flask et Python permettent une interface locale sans service cloud.
- pyodbc permet de connecter l'application à SQL Server.
- Les scripts SQL et la génération de données fournissent une base de travail technique.
- Les ressources historiques restent disponibles pour comparaison.

## Écarts constatés ou à vérifier

- L'ancienne activité de détection de joueurs ne rendait pas assez visible, pour un visiteur novice, le lien entre la question et les opérations SQL.
- La pertinence du nouveau scénario doit être validée par l'enseignant.
- Le livre *SQL Server 2022* de J. Poirier n'a pas été consulté directement dans les fichiers accessibles. Aucun chapitre ou numéro de page n'est donc attribué.
- La présence du générateur ne prouve pas que dix millions de lignes ont été insérées. Le contrôle doit être exécuté sur SQL Server.
- La durée de cinq à huit minutes est une cible et doit être mesurée avec des personnes.
- L'installation et les performances sur le PC de Sébeillon restent à tester.

## Risques techniques

- Le poste cible peut avoir un nom d'instance SQL Server différent.
- Le pilote ODBC peut ne pas être installé.
- Dix millions de lignes demandent du temps, de l'espace disque et une marge pour les index.
- Une interruption pendant la génération doit être suivie d'un contrôle du nombre de lignes avant reprise.
- Le mode simulation ne doit jamais être présenté comme une exécution réelle de SQL Server.

## Questions pour l'enseignant

1. Le thème du cinéma et l'analyse de réservations sont-ils pertinents pour les cours ICT ?
2. Les jointures, agrégations, tris et fonctions de date correspondent-ils aux notions déjà étudiées ?
3. Le volume de dix millions de réservations synthétiques est-il acceptable pour illustrer la gestion d'un grand ensemble de données ?
4. La progression proposée est-elle adaptée à des adolescents et parents qui découvrent la formation ?
5. Le parcours de trois défis et la durée visée sont-ils acceptables ?

## Limite de cet audit

Cet audit décrit les ressources et la refonte accessibles sur la branche de travail. Il ne remplace pas une exécution locale de SQL Server, une validation pédagogique ou une inspection physique du PC cible.
