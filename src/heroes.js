// Hero manifest. One entry per playable character. Asset names are fixed — see docs/SKILL.md "Adding a hero".
export const HEROES = {
  maya: {
    name: 'Maya', tagline: 'Fast. Confident. Has a plan.', card: 'cyan', available: true,
    art: {
      front: 'assets/maya/stand-front.png', quarter: 'assets/maya/stand-quarter.png',
      typing: 'assets/maya/pose-typing.png', phone: 'assets/maya/pose-phone.png',
      alarm: 'assets/maya/pose-alarm.png', slumped: 'assets/maya/pose-slumped.png',
      calm: 'assets/maya/face-calm.png', thinking: 'assets/maya/face-thinking.png', worried: 'assets/maya/face-worried.png',
      shocked: 'assets/maya/face-shocked.png', exhausted: 'assets/maya/face-exhausted.png', relieved: 'assets/maya/face-relieved.png',
    },
  },
  leo: { name: 'Leo', tagline: 'Careful. Curious. Also has a plan.', card: 'mag', available: false, art: {} },
};
