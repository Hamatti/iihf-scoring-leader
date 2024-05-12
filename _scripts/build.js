const fs = require("fs");

let raw_games = JSON.parse(
  fs.readFileSync("_data/games.json", {
    encoding: "utf8",
    flag: "r",
  })
);

let goals = raw_games.flatMap((game) => game.goals);

let points = goals.reduce((acc, current) => {
  let goal = current.goal;

  let scorer_name = `${goal.first} ${goal.last}`;
  if (scorer_name in acc) {
    acc[scorer_name].goals += 1;
    acc[scorer_name].points += 1;
  } else {
    acc[scorer_name] = {
      goals: 1,
      assists: 0,
      points: 1,
    };
  }

  current.assists.forEach((assist) => {
    let player = `${assist.first} ${assist.last}`;
    if (player in acc) {
      acc[player].assists += 1;
      acc[player].points += 1;
    } else {
      acc[player] = { assists: 1, goals: 0, points: 1 };
    }
  });
  return acc;
}, {});

let participants = JSON.parse(
  fs.readFileSync("_data/participants.json", {
    encoding: "utf8",
    flag: "r",
  })
);

let scores = [];
participants.forEach((participant) => {
  let finn = {
    participant: participant.name,
    flag: "🇫🇮",
    player: {
      name: participant.finns.name,
      bet_points: participant.finns.points,
      goals: points[participant.finns.name]?.goals || 0,
      assists: points[participant.finns.name]?.assists || 0,
      points: points[participant.finns.name]?.points || 0,
    },
  };

  let all = {
    participant: participant.name,
    flag: "🌎",
    player: {
      name: participant.all.name,
      bet_points: participant.all.points,
      goals: points[participant.all.name]?.goals || 0,
      assists: points[participant.all.name]?.assists || 0,
      points: points[participant.all.name]?.points || 0,
    },
  };

  scores.push(finn);
  scores.push(all);
});

scores.sort(
  (a, b) => b.player.points - a.player.points || b.player.goals - a.player.goals
);

fs.writeFileSync("_data/scores.json", JSON.stringify(scores));
